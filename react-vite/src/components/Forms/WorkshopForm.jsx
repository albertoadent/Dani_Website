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

export default function WorkshopForm() {
  const { workshopTypeId } = useParams();
  const type = useSelector(selectWorkshopTypeById(workshopTypeId));
  const dispatch = useDispatch();
  const [selectedDate, setSelectedDate] = useState(new Date());
  const client = useSelector((state) => state.session.client);
  const navigate = useNavigate();

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

  async function handleSubmit() {
    console.log({
      startDate: new Date(selectedDate).toISOString(),
      workshopTypeId: Number(workshopTypeId),
      clientId: Number(client.id),
    });
    await dispatch(
      postWorkshop({
        startDate: new Date(selectedDate).toISOString(),
        workshopTypeId: Number(workshopTypeId),
        clientId: Number(client.id),
      })
    );
    setSelectedDate(null);
    // navigate("/");
  }

  useEffect(() => {
    dispatch(fetchWorkshopType(workshopTypeId));
  }, [dispatch, workshopTypeId]);

  return (
    <div className="w-full mx-0 mt-[-2%] pb-96 flex flex-col items-center gap-3 pb-32 bg-[url(/vines.png)] bg-cover">
      <h1 className="text-xl font-bold underline bg-muted p-2 w-full text-center rounded text-popover">{type?.type}</h1>
      <h2 className="bg-[var(--muted-foreground)] p-2 rounded">${type?.price} per session</h2>
      <div className="w-full flex flex-col justify-center items-center pt-2 pb-[16rem] bg-[var(--muted-foreground)] rounded-xl">
      <h2 className="text-input p-1">When would you like to schedule this workshop?</h2>
        <DatePicker
          dateFormat="MMMM-dd-YYYY hh:mm a"
          selected={selectedDate}
          value={selectedDate}
          onChange={handleDateChange}
          timeIntervals="60"
          showTimeSelect
          className="w-96 justify-center text-center text-popover bg-secondary"
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
        />
      </div>
      {selectedDate && <ClientForm />}
      {client && selectedDate && <button className="bg-card text-popover p-1 rounded" onClick={handleSubmit}>SUBMIT</button>}
    </div>
  );
}
