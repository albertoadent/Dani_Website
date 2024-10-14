import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link, useNavigate } from "react-router-dom";
import {
  fetchPages,
  deletePage,
  postPage,
  publishPage,
  unpublishPage,
} from "../redux/page";
import { FaPlus, FaMinus } from "react-icons/fa";
import { useModal } from "../context/Modal";
import { fetchTemplates } from "../redux/templates";
import NewPage from "../components/Forms/PageForm";

function PageCard({ id, name, url, isPublic }) {
  const dispatch = useDispatch();

  function handleDeletePage() {
    dispatch(deletePage(id));
  }

  function handlePublishPage() {
    dispatch(publishPage(id));
  }

  function handleUnPublishPage() {
    dispatch(unpublishPage(id));
  }

  return (
    <div className="flex h-24 border-popover border rounded w-3/4 justify-center align-center items-center gap-2 p-2">
      <div className="text-center w-full flex flex-col gap-2">
        <h1>{name}</h1>
        <div className="flex justify-evenly">
          <Link
            to={`/${url == "main" ? "" : `${url}/preview`}`}
            className="border rounded p-1 w-16 h-9 bg-muted text-ring"
          >
            {url == "main" ? "Visit" : "Preview"}
          </Link>
          <Link
            to={`${url || "main"}/edit/`}
            className="border rounded p-1 w-16 h-9 bg-ring"
          >
            Edit
          </Link>
          {name.toLowerCase() != "main" && (
            <div className="border rounded p-1 w-16 h-9 bg-destructive text-popover">
              <button onClick={handleDeletePage}>Delete</button>
            </div>
          )}
          {name.toLowerCase() != "main" && isPublic && (
            <div className="border rounded p-1 w-16 h-9 bg-accent text-popover text-sm flex">
              <button onClick={handleUnPublishPage}>Suspend</button>
            </div>
          )}
          {name.toLowerCase() != "main" && !isPublic && (
            <div className="border rounded p-1 w-16 h-9 bg-accent text-popover">
              <button onClick={handlePublishPage}>Publish</button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function DisplayPages() {
  const pages = useSelector((state) => state.pages);
  const dispatch = useDispatch();
  const [pagesArray, setPagesArray] = useState(Object.values(pages || {}));
  const { setModalContent } = useModal();
  const user = useSelector((state) => state.session.user);
  const navigate = useNavigate();

  if (!user) {
    setTimeout(() => navigate("/"), 3000);

    return (
      <div>
        <h3 className="text-xl text-center m-4 p-2">Forbidden</h3>
        <h2 className="text-center">Navigating home...</h2>
      </div>
    );
  }

  useEffect(() => {
    setPagesArray(Object.values(pages));
  }, [pages]);

  useEffect(() => {
    dispatch(fetchPages());
    dispatch(fetchTemplates());
  }, [dispatch]);

  function createNewPage() {
    setModalContent(<NewPage />);
  }

  return (
    <div className="flex flex-col items-center justify-center align-center content-center gap-2">
      {pagesArray.map(({ name, id, isPublic }) => (
        <PageCard
          name={name}
          url={name.toLowerCase()}
          id={id}
          key={id}
          isPublic={isPublic}
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
