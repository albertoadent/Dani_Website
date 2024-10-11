import { useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  deleteClient,
  getClient,
  removeClient,
  postClient,
} from "../../redux/session";

function InputField({
  value,
  setValue,
  label,
  error,
  inputType = "text",
  className = "flex flex-col justify-center",
  inputClassName = "text-popover bg-muted",
}) {
  return (
    <div className={className}>
      <h3>{label}</h3>
      <input
        type={inputType}
        className={inputClassName}
        value={value}
        onChange={(e) => setValue(e.target.value)}
      />
      {error && <p>{error}</p>}
    </div>
  );
}

export default function ClientForm() {
  const placeholderFormat = (str) =>
    `${str}`
      .padEnd(10, "_")
      .split("")
      .map((char, index) => {
        if (index == 0) {
          return "(" + char;
        }
        if (index == 2) {
          return char + ")-";
        }
        if (index == 5) {
          return char + "-";
        }
        return char;
      })
      .join("");
  const client = useSelector((state) => state.session.client);

  const [firstName, setFirstName] = useState(client?.firstName);
  const [lastName, setLastName] = useState(client?.lastName);
  const [phoneNumber, setPhoneNumber] = useState(client?.phoneNumber);
  const [numberPlaceholder, setNumberPlaceholder] = useState(
    client?.phoneNumber
      ? placeholderFormat(client?.phoneNumber)
      : "(___)-___-____"
  );
  const [email, setEmail] = useState(client?.email);
  const [address, setAddress] = useState(client?.location?.address);
  const [city, setCity] = useState(client?.location?.city);
  const [state, setState] = useState(client?.location?.state);
  const [country, setCountry] = useState(client?.location?.country);
  const [newClient, setNewClient] = useState(false);
  const [error, setError] = useState("");
  const [method, setMethod] = useState("email");

  const dispatch = useDispatch();

  async function handleReturningClient() {
    if (!(phoneNumber && email)) {
      setError("Please fill in the required fields");
      setNewClient(true);
      return;
    } else {
      setError("");
    }
    try {
      await dispatch(
        getClient({
          firstName,
          lastName,
          phoneNumber: Number(phoneNumber),
          email,
        })
      );
    } catch (e) {
      setError(
        e?.message?.includes("not found")
          ? "Client was not found in the database. Please fill out the following information"
          : Object.values(e.errors || {}).join("\n")
      );
      setNewClient(true);
    }
  }

  function handleNewClient() {
    try {
      dispatch(
        postClient({
          firstName,
          lastName,
          phoneNumber: Number(phoneNumber),
          email,
          address,
          city,
          state,
          country,
          preferredMethodOfCommunication: method,
        })
      );
    } catch (e) {
      alert(e.message);
      setNewClient(true);
    }
  }

  function handleSetNumber(e) {
    const inputNum = e.target.value;

    if (inputNum.length > 1) {
      if (inputNum.length > 10) {
        setPhoneNumber(Number(inputNum.slice(inputNum.length - 10)));
        setNumberPlaceholder(
          placeholderFormat(inputNum.slice(inputNum.length - 10))
        );
      } else {
        setPhoneNumber(Number(inputNum));
        setNumberPlaceholder(placeholderFormat(inputNum));
      }

      return;
    }

    const digits = new Array(10).fill(true);
    if (!digits[inputNum]) {
      return;
    }
    const numString = String(numberPlaceholder)
      .replace(/[()-]/g, "")
      .replace("_", inputNum)
      .replace(/_/g, "");

    setPhoneNumber(Number(numString));
    setNumberPlaceholder(placeholderFormat(numString));
  }

  function handleBackspace(e) {
    if (e.key === "Backspace") {
      setNumberPlaceholder((prev) => prev.replace(/(\d)(?!.*\d)/, "_"));
      setPhoneNumber((prev) => prev / 10);
    }
  }

  if (!client) {
    return (
      <div className="flex flex-col gap-2 w-96 bg-[var(--muted-foreground)] rounded-xl p-10">
        <InputField
          label={"First name (required)"}
          value={firstName}
          setValue={setFirstName}
        />
        <InputField
          label={"Last name (required)"}
          value={lastName}
          setValue={setLastName}
        />
        <div>
          <h3>{"Phone number (required)"}</h3>
          <input
            placeholder={numberPlaceholder}
            value={() => null}
            onChange={handleSetNumber}
            className="text-popover bg-muted focus:text-popover focus:bg-muted"
            style={{ caretColor: "transparent" }}
            onKeyDown={handleBackspace}
            autoComplete="tel"
          />
        </div>
        <InputField
          label={"Email (required)"}
          value={email}
          setValue={setEmail}
        />
        <p>{!!error && error}</p>
        <button
          className="bg-[var(--secondary-foreground)] text-popover p-1 rounded"
          onClick={handleReturningClient}
        >
          I am a Returning client
        </button>
        <button
          className="bg-card text-popover p-1 rounded"
          onClick={() => setNewClient((prev) => !prev)}
        >
          {!newClient ? "I am a New Client" : "Close Location Information"}
        </button>
        {newClient && (
          <div className="flex flex-col gap-2">
            <div className="w-full flex flex-col items-center">
              <h1>Preferred Method of Communication</h1>
              <select
                value={client?.preferredMethodOfCommunication || method}
                onChange={(e) => setMethod(e.target.value)}
                id="method"
                className="bg-accent justify-center w-64 text-center px-0"
              >
                <option value="email">Email</option>
                <option value="call">Call</option>
                <option value="text">Text</option>
              </select>
            </div>
            <InputField
              label={"Address (required)"}
              value={address}
              setValue={setAddress}
            />
            <InputField
              label={"City (required)"}
              value={city}
              setValue={setCity}
            />
            <InputField
              label={"State (required)"}
              value={state}
              setValue={setState}
            />
            <InputField
              label={"Country (required)"}
              value={country}
              setValue={setCountry}
            />
            <button
              className="bg-card text-popover p-1 rounded"
              onClick={handleNewClient}
            >
              Submit
            </button>
          </div>
        )}
      </div>
    );
  }

  function handleDifferentClient() {
    dispatch(removeClient());
  }

  function handleDeleteClient() {
    dispatch(deleteClient());
    setFirstName("");
    setLastName("");
    setEmail(""), setMethod("email"), setAddress("");
    setCity("");
    setCountry("");
    setState("");
    setPhoneNumber(null);
    setNewClient(null);
  }

  return (
    <div className="bg-primary p-5 w-full justify-center items-center flex flex-col gap-2">
      <h1>Client Name: {`${client.firstName} ${client.lastName}`}</h1>
      <div className="flex justify-evenly w-full">
        <button
          className="bg-card text-popover p-1 rounded"
          onClick={handleDifferentClient}
        >
          Different Client
        </button>
        <button
          className="bg-card text-popover p-1 rounded"
          onClick={handleDeleteClient}
        >
          Delete My Data
        </button>
      </div>
    </div>
  );
}
