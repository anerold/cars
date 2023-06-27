import logging
from datetime import datetime, timezone

import requests

logger = logging
logger.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s|%(name)s|] %(message)s",
)


class TestAPI:
    def __init__(self, url: str, port: int) -> None:
        self.url = f"{url}:{port}"

    def add_car(self, car: dict) -> int:
        logger.info("Adding new car")
        endpoint = "/car/add"
        response = requests.post(self.url + endpoint, json=car)
        logger.debug(response.json())
        return response.status_code

    def update_car(self, car_info: dict) -> int:
        logger.info("Updating car")
        endpoint = "/car/update"
        response = requests.put(self.url + endpoint, json=car_info)
        logger.debug(response.json())
        return response.status_code

    def remove_car(self, car) -> int:
        logger.info("Removing car")
        endpoint = "/car/remove"
        response = requests.delete(self.url + endpoint, json=car)
        logger.debug(response.json())
        return response.status_code

    def get_all_cars(self) -> tuple[int, list[dict[str, str]]]:
        logger.info("Getting all cars")
        endpoint = "/car/cars"
        response = requests.get(self.url + endpoint)
        logger.debug(response.json())
        return response.status_code, response.json()

    def make_reservation(self, reservation: dict) -> tuple[int, list[dict[str, str]]]:
        logger.info("Making reservation")
        endpoint = "/reservation/make_reservation"
        response = requests.post(self.url + endpoint, json=reservation)
        logger.debug(response.json())
        return response.status_code, response.json()

    def get_all_reservations(self) -> tuple[int, list[dict[str, str]]]:
        logger.info("Getting all reservations")
        endpoint = "/reservation/reservations"
        response = requests.get(self.url + endpoint)
        logger.debug(response.json())
        return response.status_code, response.json()


def find_car_in_all_cars(sample_car: dict) -> None:
    status, cars = tester.get_all_cars()
    assert status == 200, "Getting all cars failed"
    # check whether our car is present in all cars
    for car in cars:
        if car == sample_car:
            break
    else:
        raise AssertionError("Created car is not present in all cars list!")


if __name__ == "__main__":
    sample_car = {"maker": "company", "model": "car_model", "uid": "C112"}
    tester = TestAPI("http://localhost", 8000)
    # first create a car
    assert tester.add_car(sample_car) == 201, "Car creation failed"
    # get all cars and find our car in them
    find_car_in_all_cars(sample_car)
    # verify we can't create same car again
    assert tester.add_car(sample_car) == 409, "Added same car twice"
    # update our car
    new_uid = "C123456"
    new_maker = "another_company"
    new_model = "another_model"
    assert (
        tester.update_car(
            {"uid": sample_car["uid"], "new_uid": new_uid, "new_maker": new_maker, "new_model": new_model}
        )
        == 200
    ), "Car update failed"
    # verify we can't update car to an uid that already exists
    assert (
        tester.update_car(
            {"uid": new_uid, "new_uid": new_uid, "new_maker": new_maker, "new_model": new_model}
        )
        == 409
    ), "Updated car to an existing uid"
    sample_car["uid"] = new_uid
    sample_car["maker"] = new_maker
    sample_car["model"] = new_model
    # verify car is updated
    find_car_in_all_cars(sample_car)

    ## Reservation testing
    # +10 because reservation cannot be in the past and datetime.utcnow() can already be in the past by the time api is called
    now = int(datetime.now(timezone.utc).timestamp()) + 10
    offset = 60
    status, response = tester.make_reservation({"timestamp_start": now, "timestamp_end": now + offset})
    assert status == 201, "Car reservation failed"
    # verify it returned correct reservation time
    assert (
        int(datetime.strptime(response["start"], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc).timestamp()) == now
    ), "Reservation start time does not match"
    assert (
        int(datetime.strptime(response["end"], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc).timestamp())
        == now + offset
    ), "Reservation end time does not match"
    # get all reservations and also verify our reservation is present
    status, response = tester.get_all_reservations()
    assert status == 200, "Getting all reservations failed"
    for reservation in response:
        if reservation["timestamp_start"] == now and reservation["timestamp_end"] == now + offset:
            break
    else:
        raise AssertionError("Newly created reservation is not present in list of all reservations")
    ## check reservation validations
    # start in past
    status, response = tester.make_reservation({"timestamp_start": 0, "timestamp_end": 100})
    assert status == 400, "Reserved car in the past"
    # start in future more tha 24 hours
    status, response = tester.make_reservation({"timestamp_start": now + 25*60*60, "timestamp_end": now + offset + 25*60*60})
    assert status == 400, "Reserved car too far in the future"
    # end later than start
    status, response = tester.make_reservation({"timestamp_start": now + offset, "timestamp_end": now})
    assert status == 400, "Reservation end sooner than start"

    ## lastly delete the test car (in order to cleanup and also in order to test delete function)
    assert tester.remove_car({"uid": sample_car["uid"]}) == 200, "Car deletion failed"
    try:
        # check our car disappeared from all cars
        find_car_in_all_cars(sample_car)
    except AssertionError:
        pass
    else:
        raise AssertionError("Car was not removed")
    logger.info("---TEST SUCCESSFUL---")
