import { useDispatch, useSelector } from "react-redux";
import {
  fetchWorkshopTypes,
  selectWorkshopTypesArray,
} from "../../redux/workshops";
import { useEffect } from "react";
import WorkshopCard from "../Cards/WorkshopCard";

export default function Workshops() {
  const types = useSelector(selectWorkshopTypesArray);
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(fetchWorkshopTypes());
  }, [dispatch]);

  return (
    <div className="mt-32 top-1">
      <h1 className="fixed top-[5.7rem] left-[50%] transform -translate-x-1/2 -translate-y-1/2 justify-center bg-card text-popover border-t-0 border-r-2 border-b-2 border-l-2 border-accent rounded-lg text-xl font-bold p-2 z-0">
        Workshops
      </h1>
      <div className="w-3/5 m-auto flex flex-col justify-center items-center align-center border-l-8 border-r-8 border-t-8 rounded-t-lg border-input">
        {types &&
          types?.map((type) => (
            <WorkshopCard
              header={type?.type}
              text={type?.description}
              linkTo={`/workshops/${type?.id}`}
            />
          ))}
      </div>
    </div>
  );
}
