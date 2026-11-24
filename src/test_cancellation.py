
from cancellation import (
    calculate_guest_refund,
    calculate_host_cancellation
)


def test_guest_refund_30_hours_before():
    refund = calculate_guest_refund(2000, 30)
    assert refund == 1500


def test_guest_refund_more_than_48_hours():
    refund = calculate_guest_refund(2000, 60)
    assert refund == 2000


def test_guest_refund_after_start():
    refund = calculate_guest_refund(2000, 0)
    assert refund == 0


def test_host_cancellation_within_24_hours():
    credit, penalty = calculate_host_cancellation(12)
    assert credit == 500
    assert penalty == 1000

