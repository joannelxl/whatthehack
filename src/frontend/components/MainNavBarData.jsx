import HomeIcon from "@mui/icons-material/Home";
import LinkIcon from "@mui/icons-material/Link";
import SementicSearchIcon from "@mui/icons-material/FileCopy";
import "./MainNavBar.css";

export const MainNavBarData = [
  {
    icon: <HomeIcon class="svg-icon" />,
    title: "Home",
    link: "home",
  },

  {
    icon: <LinkIcon class="svg-icon" />,
    title: "URL Query",
    link: "urlquery",
  },
  {
    icon: <SementicSearchIcon class="svg-icon" />,
    title: "Local Sementic Search",
    link: "localsementicsearch",
  },
];
