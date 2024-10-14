import { useParams } from "react-router-dom";
import Templates from "../Templates";
import { useDispatch, useSelector } from "react-redux";
import { fetchPages, selectPageByName } from "../../redux/page";
import { useEffect } from "react";
import { fetchTemplates, selectTemplateById } from "../../redux/templates";

export default function PageNotFound() {
  return <h1 className="flex justify-center p-10 text-lg">Page Not Found</h1>;
}

export function ReRoute({ isPreview }) {
  const { pageName } = useParams();
  const page = useSelector((state) => selectPageByName(state, pageName));
  const user = useSelector((state) => state.session.user);
  const template = useSelector(selectTemplateById(page?.templateId));
  const dispatch = useDispatch();
  const viewable = !!(page?.isPublic || (isPreview && user));

  useEffect(() => {
    dispatch(fetchTemplates());
    dispatch(fetchPages());
  }, [dispatch]);

  if (!page || !viewable) {
    return <PageNotFound />;
  }

  const Template =
    Templates[template?.name] || Templates[pageName] || Templates.main;
  return <Template page={page} />;
}
