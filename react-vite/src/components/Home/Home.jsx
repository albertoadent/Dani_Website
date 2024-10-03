import { useNavigate } from "react-router-dom";
import "./home.css";
import { useSelector } from "react-redux";
import { useModal } from "../../context/Modal";
import LoginFormModal from "../LoginFormModal";
import { useEffect, useState } from "react";
import MainTemplate from "../Templates/MainTemplate";

const Home = () => {
  const user = useSelector((state) => state.session.user);
  const nav = useNavigate();
  const { setModalContent } = useModal();
  const [page, setPage] = useState({ content: [] });

  useEffect(() => {
    fetch("/api/pages/1").then((res) => res.json()).then(setPage);
  }, []);

  return (
    <div>
      <MainTemplate page={page}/>
    </div>
  );
};

export default Home;
