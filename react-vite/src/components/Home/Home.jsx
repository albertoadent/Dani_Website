import "./home.css";
import { useDispatch, useSelector } from "react-redux";
import { useEffect, useState } from "react";
import MainTemplate from "../Templates/MainTemplate";
import { fetchPage, selectPageById } from "../../redux/page";

const Home = () => {
  const page = useSelector(selectPageById(1));
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(fetchPage(1));
  }, [dispatch]);

  return (
    <div>
      <MainTemplate page={page} />
    </div>
  );
};

export default Home;
