from __future__ import annotations
import sys
from google.cloud import compute_v1
from google.api_core.extended_operation import ExtendedOperation
from typing import Any
from random import randint
import sys
import argparse


def wait_for_extended_operation(
        operation: ExtendedOperation, verbose_name: str = "operation", timeout: int = 100
) -> Any:
    result = operation.result(timeout=timeout)

    if operation.error_code:
        print(
            f"Error during {verbose_name}: [Code: {operation.error_code}]: {operation.error_message}",
            file=sys.stderr,
            flush=True,
        )
        print(f"Operation ID: {operation.name}", file=sys.stderr, flush=True)
        raise operation.exception() or RuntimeError(operation.error_message)

    if operation.warnings:
        print(f"Warnings during {verbose_name}:\n", file=sys.stderr, flush=True)
        for warning in operation.warnings:
            print(f" - {warning.code}: {warning.message}", file=sys.stderr, flush=True)

    return result


def list_disks(
        project_id: str, zone: str,
) -> Iterable[compute_v1.Disk]:
    disk_client = compute_v1.DisksClient()
    request = compute_v1.ListDisksRequest()
    request.project = project_id
    request.zone = zone
    # request.filter = filter_
    return disk_client.list(request)


def create_empty_disk(
        disk_name: str,
        project_id: str,
        zone: str
):
    disk = compute_v1.Disk()
    disk.name = disk_name
    disk_client = compute_v1.DisksClient()
    operation = disk_client.insert(project=project_id, zone=zone, disk_resource=disk)

    wait_for_extended_operation(operation, "disk creation")

    # return disk_client.get(disk=disk.name)


def resize_disk(project_id: str, disk_link: str, new_size_gb: int):
    request.disk = "test-disk91"
    request.project = project_id
    request.zone = "us-central1-a"
    request.disks_resize_request_resource = compute_v1.DisksResizeRequest()
    request.disks_resize_request_resource.size_gb = new_size_gb
    operation = disk_client.resize(request)
    wait_for_extended_operation(operation, "disk resize")


''' 
def authenticate_implicit_with_adc(project_id="cw-academy-sandbox-widad"):
    disklist =list_disks(project_id=project_id,zone="us-central1-a")
    print("List of disk")
    [print(d)for d in disklist]
    disk_name = "test-disk"+str(randint(1,999))
    create_empty_disk(disk_name=disk_name,project_id=project_id,zone="us-central1-a")

'''


def delete_disk(project_id: str, zone: str, disk_name: str) -> None:
    disk_client = compute_v1.DisksClient()
    operation = disk_client.delete(project=project_id, zone=zone, disk=disk_name)
    wait_for_extended_operation(operation, "disk deletion")


# def authenticate_implicit_with_adc():
def main():
    project_id = "cw-academy-sandbox-widad"
    parser = argparse.ArgumentParser()
    # Add optional arguments
    parser.add_argument("project_id",
                        type=str, , nargs='?')
    # parser.add_argument("disk_name", help="name of d",type=str)
    parser.add_argument('-c', help="create disk", action="store_true")
    parser.add_argument('-l', help="list disks", action="store_true")
    args = parser.parse_args()
    if args.c:
        disk_name = input("Enter disk name")
        zone = input("Enter zone")
        create_empty_disk(project_id=project_id, zone=zone, disk_name=disk_name)
    elif args.l:
        zone = input("Enter zone")
        disklist = list_disks(project_id=project_id, zone=zone)
        print("List of disks")
        [print(d) for d in disklist]


if __name__ == "__main__":
    main()
