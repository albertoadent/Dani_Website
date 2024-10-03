import { useState, useEffect, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { FaUserCircle } from "react-icons/fa";
import { thunkLogout } from "../../redux/session";
import OpenModalMenuItem from "../Navigation/OpenModalMenuItem.jsx";
import LoginFormModal from "../LoginFormModal";
import SignupFormModal from "../SignupFormModal";
import { useNavigate } from "react-router-dom";

function ProfileButton() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [showMenu, setShowMenu] = useState(false);
  const user = useSelector((store) => store.session.user);
  const ulRef = useRef();

  const toggleMenu = (e) => {
    e.stopPropagation();
    setShowMenu(!showMenu);
  };

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

  const closeMenu = () => {
    setShowMenu(false);
  };

  const logout = (e) => {
    e.preventDefault();
    dispatch(thunkLogout());
    closeMenu();
    navigate("/");
  };

  return (
    <>
      <button onClick={toggleMenu}>
        <FaUserCircle className="text-popover" size={24} />
      </button>

      {showMenu && (
        <ul
          className="absolute z-10 bg-card flex flex-col right-0 mr-4 gap-4 shadow-shadow text-base border px-3 py-2 rounded-lg"
          ref={ulRef}
        >
          {user ? (
            <>
              <li className="hover:cursor-pointer">
                <div className="flex flex-col gap-2 border-b-2 border-border pb-2">
                  <span>{user?.name || "No name"}</span>
                  <span>{user.email}</span>
                </div>
              </li>

              <li className="cursor-pointer">
                <button onClick={logout}>Log Out</button>
              </li>
            </>
          ) : (
            <>
              <li className="cursor-pointer">
                <OpenModalMenuItem
                  itemText="Log In"
                  onItemClick={closeMenu}
                  modalComponent={<LoginFormModal />}
                />
              </li>

              <li className="cursor-pointer">
                <OpenModalMenuItem
                  itemText="Sign Up"
                  onItemClick={closeMenu}
                  modalComponent={<SignupFormModal />}
                />
              </li>
            </>
          )}
        </ul>
      )}
    </>
  );
}

export default ProfileButton;
