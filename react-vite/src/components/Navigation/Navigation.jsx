import { useSelector } from "react-redux";
import ProfileButton from "./ProfileButton";
import { NavLink } from "react-router-dom";
import { useEffect, useState } from "react";
import Logo from "./Logo";

const Navigation = () => {
  const user = useSelector((store) => store.session.user);
  const [showMenu, setShowMenu] = useState(false);

  useEffect(() => {
    if (!showMenu) return;

    const closeMenu = (e) => {
      if (ulRef.current && !ulRef.current.contains(e.target)) {
        setShowMenu(false);
      }
    };

    document.addEventListener("click", closeMenu);

    return () => document.removeEventListener("click", closeMenu);
  }, [showMenu]);

  return (
    <ul className="flex justify-between px-8 pt-4 pb-4 text-lg bg-card">
      <li>
        <NavLink to="/">
          <Logo className="text-background" />
        </NavLink>
      </li>
      <li>
        <ProfileButton />
      </li>
    </ul>
  );
};

export default Navigation;
