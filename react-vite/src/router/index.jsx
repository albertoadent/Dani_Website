import { createBrowserRouter } from "react-router-dom";
import LoginFormPage from "../components/LoginFormPage";
import SignupFormPage from "../components/SignupFormPage";
import Layout from "./Layout";
import Home from "../components/Home/Home";
import Workshops from "../components/Workshops/Workshops";
import WorkshopForm from "../components/Forms/WorkshopForm";

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
        path: "*",
        element: (
          <h1 className="flex justify-center p-10 text-lg">Page Not Found</h1>
        ),
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
    ],
  },
]);
