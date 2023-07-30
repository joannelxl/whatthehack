import HomeIcon from "@mui/icons-material/Home";
import ChatIcon from "@mui/icons-material/Chat";
import LinkIcon from "@mui/icons-material/Link";
import SummarizeIcon from "@mui/icons-material/Summarize";
import FindInPageIcon from "@mui/icons-material/FindInPage";
import TranslateIcon from "@mui/icons-material/Translate";
import YouTubeIcon from "@mui/icons-material/YouTube";
import LanguageIcon from "@mui/icons-material/Language";
import "./MainNavBar.css";

export const MainNavBarData = [
  {
    icon: <HomeIcon class="svg-icon" />,
    title: "Home",
    link: "home",
  },
  // {
  //   icon: <ChatIcon class="svg-icon" />,
  //   title: "Chat",
  //   link: "chat",
  // },
  // {
  //   icon: <SummarizeIcon class="svg-icon" />,
  //   title: "Batch Summarization",
  //   link: "summarization",
  // },
  // {
  //   icon: <FindInPageIcon class="svg-icon" />,
  //   title: "Batch Keyword Extraction",
  //   link: "keyword",
  // },
  // {
  //   icon: <TranslateIcon class="svg-icon" />,
  //   title: "Batch Translation",
  //   link: "translation",
  // },
  // {
  //   icon: <LanguageIcon class="svg-icon" />,
  //   title: "Real-Time Web Search / URL Query",
  //   link: "websearch",
  // },
  {
    icon: <LinkIcon class="svg-icon" />,
    title: "Real-Time URL Function-Based Query",
    link: "urlquery",
  },
  {
    icon: <YouTubeIcon class="svg-icon" />,
    title: "Video Transcription",
    link: "youtube",
  },
];
