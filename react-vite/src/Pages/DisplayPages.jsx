import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link } from "react-router-dom";
import { fetchPages, deletePage, postPage } from "../redux/page";
import { FaPlus, FaMinus } from "react-icons/fa";
import { useModal } from "../context/Modal";

function NewPage() {
  const [name, setName] = useState(null);
  const [template, setTemplate] = useState();
  const dispatch = useDispatch();
  const { closeModal } = useModal();
  return (
    <div className="flex flex-col justify-center items-center">
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        type="text"
        placeholder="New Page Name"
      />
      <button
        onClick={() => {
          dispatch(postPage({ name }));
          closeModal();
        }}
        className="bg-muted text-popover rounded border-accent border"
      >
        Create New Page!
      </button>
    </div>
  );
}

function PageCard({ id, name, url }) {
  const dispatch = useDispatch();

  function handleDeletePage(e) {
    e.stopPropagation();
    dispatch(deletePage(id));
    e.stopPropagation();
  }

  return (
    <div className="flex h-20 border-popover border rounded w-3/4 justify-center align-center items-center gap-2">
      <Link to={url} className="text-center w-1/2">
        {name}
      </Link>
      {name.toLowerCase() != "main" && (
        <FaMinus
          onClick={handleDeletePage}
          className="text-destructive border border-popover p-1 rounded w-1/2 h-full"
        />
      )}
    </div>
  );
}

export default function DisplayPages() {
  const pages = useSelector((state) => state.pages);
  const dispatch = useDispatch();
  const [pagesArray, setPagesArray] = useState(Object.values(pages || {}));
  const { setModalContent } = useModal();

  useEffect(() => {
    setPagesArray(Object.values(pages));
  }, [pages]);

  useEffect(() => {
    dispatch(fetchPages());
  }, [dispatch]);

  function createNewPage() {
    setModalContent(<NewPage />);
  }

  return (
    <div className="flex flex-col items-center justify-center align-center content-center gap-2">
      {pagesArray.map(({ name, id }) => (
        <PageCard
          name={name}
          url={`/${name.toLowerCase() == "main" ? "" : name}`}
          id={id}
          key={id}
        />
      ))}
      <button
        onClick={createNewPage}
        className="flex h-20 border-popover border rounded w-3/4 justify-center align-center items-center"
      >
        <FaPlus />
      </button>
    </div>
  );
}
