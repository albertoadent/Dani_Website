import { useEffect, useState } from "react";
import { FaMinus, FaPlus, FaArrowDown } from "react-icons/fa";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import {
  deleteContent,
  fetchPage,
  fetchPages,
  postContent,
  putContent,
  selectPageByName,
} from "../../redux/page";

export default function ContentForm({ pageId, content }) {
  const [header, setHeader] = useState(content?.header || null);
  const [subHeader, setSubHeader] = useState(content?.subHeader || null);
  const [text, setText] = useState(content?.text || null);
  const [file, setFile] = useState(content?.file || null);
  const [linkTo, setLinkTo] = useState(content?.linkTo || null);
  const [creatingNew, setCreatingNew] = useState(false);
  const [editing, setEditing] = useState(false);
  const dispatch = useDispatch();

  useEffect(() => {
    if (!pageId) {
      dispatch(fetchPages());
    } else {
      dispatch(fetchPage(pageId));
    }
  }, [dispatch]);

  function handleCreateNewContent() {
    const buildBody = {};
    if (header) {
      buildBody.header = header;
    }
    if (subHeader) {
      buildBody.subHeader = subHeader;
    }
    if (text) {
      buildBody.text = text;
    }
    if (file) {
      buildBody.file = file;
    }
    if (linkTo) {
      buildBody.linkTo = linkTo;
    }
    dispatch(postContent(pageId, buildBody));
  }

  function handleEditingContent() {
    const buildBody = {};
    if (header) {
      buildBody.header = header;
    }
    if (subHeader) {
      buildBody.subHeader = subHeader;
    }
    if (text) {
      buildBody.text = text;
    }
    if (file) {
      buildBody.file = file;
    }
    if (linkTo) {
      buildBody.linkTo = linkTo;
    }
    buildBody.id = content.id;
    dispatch(putContent(buildBody));
  }

  function handleDeleteContent() {
    dispatch(deleteContent(content.id));
    setCreatingNew(false);
    setHeader(null);
    setSubHeader(null);
    setText(null);
    setFile(null);
    setLinkTo(null);
  }

  if (!content && !creatingNew) {
    return (
      <button
        className="bg-muted w-24 h-12 text-center flex flex-col justify-center items-center rounded my-2"
        onClick={() => setCreatingNew(true)}
      >
        <FaPlus />
      </button>
    );
  }

  if (!editing && content) {
    return (
      <button
        className="bg-muted w-24 h-12 text-center flex flex-col justify-center items-center rounded my-2"
        onClick={() => setEditing(true)}
      >
        <h2>Section: {content.id.split("_")[1]}</h2>
        <FaArrowDown />
      </button>
    );
  }

  return (
    <div className="flex flex-col text-center items-center w-full border border-accent p-2 bg-primary mb-2">
      <button
        onClick={() => {
          setCreatingNew(false);
          setEditing(false);
        }}
      >
        <FaMinus />
      </button>
      {content ? (
        <h2>Section: {content.id.split("_")[1]}</h2>
      ) : (
        <h2>New Section:</h2>
      )}

      <div className="flex flex-col gap-1">
        <input
          type="text"
          placeholder="Header"
          value={header ? header : null}
          onChange={(e) => setHeader(e.target.value)}
          className="bg-secondary border text-popover p-2 placeholder-[var(--secondary-foreground)]"
        />

        <input
          type="text"
          placeholder="Sub Header"
          value={subHeader ? subHeader : null}
          onChange={(e) => setSubHeader(e.target.value)}
          className="bg-secondary border text-popover p-2 placeholder-[var(--secondary-foreground)]"
        />

        <textarea
          name="text"
          id="text"
          placeholder="Main Content"
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="bg-secondary border text-input h-48 p-2 placeholder-[var(--secondary-foreground)]"
        />

        <input
          type="text"
          placeholder="Links to this when clicked"
          value={linkTo}
          onChange={(e) => setLinkTo(e.target.value)}
          className="bg-secondary border text-popover p-2 placeholder-[var(--secondary-foreground)]"
        />

        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          className="bg-secondary border text-input p-2"
        />

        {content && (
          <button
            className="bg-accent rounded border"
            onClick={handleDeleteContent}
          >
            DELETE
          </button>
        )}

        <button
          onClick={content ? handleEditingContent : handleCreateNewContent}
          className="bg-muted text-popover rounded border"
        >
          {content ? "Update" : "Create"}
        </button>
      </div>
    </div>
  );
}
