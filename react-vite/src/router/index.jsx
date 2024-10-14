import { createBrowserRouter } from "react-router-dom";
import LoginFormPage from "../components/LoginFormPage";
import SignupFormPage from "../components/SignupFormPage";
import Layout from "./Layout";
import Home from "../components/Home/Home";
import Workshops from "../components/Workshops/Workshops";
import WorkshopForm from "../components/Forms/WorkshopForm";
import DisplayPages from "../Pages/DisplayPages";
import { Navigate } from "react-router-dom";
import { ReRoute } from "../components/NotFound/PageNotFound";
import PageNotFound from "../components/NotFound/PageNotFound";
import { EditPage } from "../components/Forms/PageForm";

export const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      {
        path: "/",
        element: <Home />,
      },
      {
        path: "login",
        element: <LoginFormPage />,
      },
      {
        path: "signup",
        element: <SignupFormPage />,
      },
      {
        path: "workshops",
        children: [
          {
            index: true,
            element: <Workshops />,
          },
          {
            path: ":workshopTypeId",
            element: <WorkshopForm />,
          },
        ],
      },
      {
        path: "pages",
        children: [
          {
            index: true,
            element: <DisplayPages />,
          },
          {
            path: ":pageName/edit",
            element: <EditPage />,
          },
        ],
      },
      {
        path: "/:pageName",
        children: [
          {
            index: true,
            element: <ReRoute />,
          },
          {
            path: "preview",
            element: <ReRoute isPreview={true} />,
          },
        ],
      },
      {
        path: "*",
        element: <PageNotFound />,
      },
    ],
  },
]);
