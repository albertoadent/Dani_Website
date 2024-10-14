import { useDispatch, useSelector } from "react-redux";
import { useModal } from "../../context/Modal";
import { useEffect, useRef, useState } from "react";
import { fetchTemplates, selectTemplateArray } from "../../redux/templates";
import {
  fetchPages,
  postPage,
  putPage,
  selectPageByName,
} from "../../redux/page";
import ContentForm from "./ContentForm";
import { Link, useParams } from "react-router-dom";

export default function NewPage() {
  const [name, setName] = useState(null);
  const [template, setTemplate] = useState(null);
  const templates = useSelector(selectTemplateArray);
  const dispatch = useDispatch();
  const { closeModal } = useModal();

  useEffect(() => {
    if (!templates.length) {
      dispatch(fetchTemplates());
    }
  }, [dispatch]);

  return (
    <div className="flex flex-col justify-center items-center gap-2">
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        type="text"
        placeholder="New Page Name"
        className="bg-ring text-popover placeholder-muted"
      />
      <select
        id="template"
        value={template}
        onChange={(e) => setTemplate(e.target.value)}
        className="bg-ring text-popover"
      >
        {[{ name: "New Template", id: null }, ...templates].map((temp) => (
          <option key={temp.id} value={temp.id}>
            {temp.name}
          </option>
        ))}
      </select>
      <button
        onClick={() => {
          if (template) {
            dispatch(postPage({ name, templateId: Number(template) || null }));
          } else {
            dispatch(postPage({ name }));
          }
          closeModal();
        }}
        className="bg-muted text-popover rounded border-accent border p-2"
      >
        Create New Page!
      </button>
    </div>
  );
}

export function EditPage() {
  const { pageName } = useParams();

  const page = useSelector((state) => selectPageByName(state, pageName));
  const dispatch = useDispatch();
  const [template, setTemplate] = useState(page?.templateId);
  const templates = useSelector(selectTemplateArray);
  const [templateName, setTemplateName] = useState(pageName || "Main");
  const originalTemplateName = pageName || "Main";
  const selectRef = useRef();

  useEffect(() => {
    if (!page) {
      dispatch(fetchPages());
    }
  }, [dispatch]);
  useEffect(() => {
    if (!templates.length) {
      dispatch(fetchTemplates());
    }
  }, [dispatch]);

  const content = [...(page?.content || []), null];

  function handleUpdateTemplateId() {
    if (templateName != originalTemplateName) {
      dispatch(putPage({ ...page, templateName: templateName }));
    } else {
      dispatch(putPage({ ...page, templateId: Number(template) }));
    }
  }

  function handleSetTemplate(e) {
    setTemplateName(e.target.value);
  }

  if (!page) {
    return <h2>Loading...</h2>;
  }

  return (
    <ul className="w-full flex flex-col items-center mb-24">
      <h1>{page?.name}</h1>
      <Link
        className="my-5 border rounded bg-ring p-2"
        to={`/${pageName}/preview`}
      >
        Preview page
      </Link>

      <div className="flex flex-col items-center border p-2 rounded mb-4">
        <h1>Template</h1>
        <select
          ref={selectRef}
          id="template"
          value={template}
          onChange={(e) => setTemplate(e.target.value)}
          className="bg-ring text-popover"
        >
          {[{ name: "New Template", id: null }, ...templates].map((temp) => (
            <option className="text-center" key={temp.id} value={temp.id}>
              {temp.name}
            </option>
          ))}
        </select>
        {selectRef?.current?.value == "New Template" && (
          <input
            type="text"
            placeholder="template name here"
            value={templateName}
            onChange={handleSetTemplate}
            className="bg-card text-input"
          />
        )}
        <button
          className="mt-2 mb-5 border rounded bg-ring p-2"
          onClick={handleUpdateTemplateId}
        >
          Update Template
        </button>
      </div>

      {content.map((con, index) => (
        <ContentForm key={index} pageId={page?.id} content={con} />
      ))}
    </ul>
  );
}
