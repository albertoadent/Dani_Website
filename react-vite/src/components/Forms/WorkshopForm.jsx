import { useDispatch, useSelector } from "react-redux";
import { useNavigate, useParams } from "react-router-dom";
import {
  fetchWorkshopType,
  postWorkshop,
  selectWorkshopTypeById,
} from "../../redux/workshops";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { useEffect, useState } from "react";
import ClientForm from "./ClientForm";
import { useModal } from "../../context/Modal";

function WorkshopConfirmationModal({
  startDate = "NO START DATE",
  duration = "NO DURATION",
  price = "0.00",
  workshopName = "NO WORKSHOP SELECTED",
  onSubmit = () => null,
}) {
  const { closeModal } = useModal();
  return (
    <div className="bg-[var(--popover-foreground)] p-2 rounded">
      <h1 className="text-center text-lg font-bold">
        Please confirm this is what you want
      </h1>
      <h2 className="text-center">Workshop: {workshopName}</h2>
      <h3 className="text-center text-secondary text-xl font-bold">${price}</h3>
      <div className="flex flex-col bg-primary rounded p-1 m-1 gap-2">
        <h2 className="text-center">The workshop will start: </h2>
        <p className="text-center">
          {startDate
            ?.split(" ")
            .slice(0, 5)
            .map((dateSection) => {
              if (dateSection.includes(":")) {
                let isAM = true;
                let time = dateSection
                  .split(":")
                  .map((time, index) => {
                    if (index == 0) {
                      if (Number(time) - 12 > 0) {
                        isAM = false;
                        return Number(time) - 12;
                      }
                    }
                    return time;
                  })
                  .slice(0, 2)
                  .join(":");
                return isAM ? time + " AM" : time + " PM";
              }
              if (dateSection.length == 2) {
                if (dateSection == "01") {
                  return "1st";
                }
                if (dateSection == "02") {
                  return "2nd";
                }
                if (dateSection == "03") {
                  return "3rd";
                }
                if (dateSection.startsWith("0")) {
                  return dateSection[1] + "th";
                }
                return dateSection + "th";
              }
              return dateSection;
            })
            .join(" ")}{" "}
        </p>
        <p className="text-center"> 
          The workshop will last{" "}
          {duration == 1 ? duration + " hour" : duration + " hours"}
        </p>
      </div>

      <div className="flex justify-evenly">
        <button className="bg-muted rounded p-1" onClick={onSubmit}>
          Yes - checkout
        </button>
        <button className="bg-muted rounded p-1" onClick={closeModal}>
          No - go back
        </button>
      </div>
    </div>
  );
}

export default function WorkshopForm() {
  const { workshopTypeId } = useParams();
  const type = useSelector(selectWorkshopTypeById(workshopTypeId));
  const dispatch = useDispatch();
  const [selectedDate, setSelectedDate] = useState(new Date());
  const client = useSelector((state) => state.session.client);
  const navigate = useNavigate();
  const { setModalContent, closeModal, modalContent } = useModal();

  const startTime = new Date(Date.now());
  startTime.setHours(7, 0, 0);
  const endTime = new Date(Date.now());
  endTime.setHours(20, 0, 0);

  function handleDateChange(date) {
    setSelectedDate(date);
  }
  const bookedDates = type?.workshops?.map((workshop) => {
    const start = new Date(workshop.startDate);
    start.setHours(start.getHours() - 1);
    const end = new Date(workshop.startDate);
    end.setHours(end.getHours() + 1);
    return [start.toISOString(), end.toISOString()];
  });

  function bookingsOnDay(d) {
    let bookings = 0;
    const onDay = new Date(d);
    for (const [date, _] of bookedDates || []) {
      const day = new Date(date);
      day.setHours(0, 0, 0, 0);
      onDay.setHours(0, 0, 0, 0);
      bookings += day.getTime() === onDay.getTime() ? 1 : 0;
    }
    return !(bookings >= 3);
  }

  function inBookedDates(d) {
    const date = new Date(d).toISOString();
    for (const [start, end] of bookedDates || []) {
      const beginning = new Date(start).getTime();
      const middle = new Date(date).getTime();
      const finish = new Date(end).getTime();
      if (beginning <= middle && middle <= finish) {
        return true;
      }
    }
    return false;
  }

  function handleSubmit() {
    async function handleConfirm() {
      await dispatch(
        postWorkshop({
          startDate: new Date(selectedDate).toISOString(),
          workshopTypeId: Number(workshopTypeId),
          clientId: Number(client.id),
        })
      );
      setSelectedDate(null);
      closeModal();
    }

    setModalContent(
      <WorkshopConfirmationModal
        startDate={String(selectedDate)}
        workshopName={type?.type}
        duration={type?.timeFrame}
        price={type?.price}
        onSubmit={handleConfirm}
      />
    );

  }

  useEffect(() => {
    dispatch(fetchWorkshopType(workshopTypeId));
  }, [dispatch, workshopTypeId]);

  return (
    <div className="w-full mx-0 mt-[-2%] pb-96 flex flex-col items-center gap-3 pb-32 bg-[url(/vines.png)] bg-cover">
      <h1 className="text-xl font-bold underline bg-muted p-2 w-full text-center rounded text-popover">
        {type?.type}
      </h1>
      <h2 className="bg-[var(--muted-foreground)] p-2 rounded">
        ${type?.price} per session
      </h2>
      <div className="w-full flex flex-col justify-center items-center pt-2 pb-[16rem] bg-[var(--muted-foreground)] rounded-xl">
        <h2 className="text-input p-1">
          When would you like to schedule this workshop?
        </h2>
        {!modalContent && (
          <DatePicker
            dateFormat="MMMM-dd-YYYY hh:mm a"
            selected={selectedDate}
            value={selectedDate}
            onChange={handleDateChange}
            timeIntervals="60"
            showTimeSelect
            className="w-96 justify-center text-center text-popover bg-secondary z-0"
            open
            showPopperArrow={false}
            minDate={Date.now()}
            maxDate={
              selectedDate
                ? new Date().setDate(new Date().getDate() + 365 + 365)
                : false
            }
            minTime={startTime}
            maxTime={endTime}
            filterDate={bookingsOnDay}
            filterTime={(date) => !inBookedDates(date)}
            readOnly
          />
        )}
      </div>
      {selectedDate && <ClientForm />}
      {client && selectedDate && (
        <button
          className="bg-card text-popover p-1 rounded"
          onClick={handleSubmit}
        >
          SUBMIT
        </button>
      )}
    </div>
  );
}
