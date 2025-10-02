import { createBrowserRouter } from "react-router-dom";

//import App from "../App";
import Login from "./login";
import HomePage from "./dashboard";


    const router = createBrowserRouter([
    //{ path: '', element: <App/> },
    { path: '', element: <Login/> },
    {path: 'dashboard', element: <HomePage/>}
    ]);

export default router;