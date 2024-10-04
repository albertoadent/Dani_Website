import { Link } from "react-router-dom";
import LinkedIn from "../../Socials/LinkedIn";
import Instagram from "../../Socials/Instagram";
import PrideFlag from "./PrideFlag";
export default function Footer() {
  const dimension = "32";
  return (
    <ul className="fixed bottom-0 text-popover border-accent bg-card flex w-full flex-col align-center content-center justify-center items-center text-sm border-t-2 gap-y-2 pt-2 pb-2">
      <li className="flex justify-center gap-3 w-full">
        <div className="border-l p-1 border-r rounded w-24 text-center">
          <Link to="/about" className="w-full">
            About
          </Link>
        </div>
        <div className="border-l p-1 border-r rounded w-24 text-center">
          <Link to="/contact" className="w-full">
            Contact
          </Link>
        </div>
        <div className="border-l p-1 border-r rounded w-24 text-center">
          <Link to="/faq" className="w-full">
            FAQ
          </Link>
        </div>
      </li>

      <li className="flex gap-1 justify-center w-full">
        <LinkedIn dimension={dimension} />
        <Instagram dimension={dimension} />
        <PrideFlag dimension={dimension} />
      </li>
    </ul>
  );
}
