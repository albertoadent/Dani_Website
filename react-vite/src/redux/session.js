import { post, jsonPost, del } from "./customFetch";

const SET_USER = "session/setUser";
const REMOVE_USER = "session/removeUser";
const SET_CLIENT = "session/setClient";
const REMOVE_CLIENT = "session/removeClient";

const setUser = (user) => ({
  type: SET_USER,
  payload: user,
});

const removeUser = () => ({
  type: REMOVE_USER,
});

const setClient = (client) => ({
  type: SET_CLIENT,
  client,
});

export const removeClient = () => ({
  type: REMOVE_CLIENT,
});

export const thunkAuthenticate = () => async (dispatch) => {
  const response = await fetch("/api/auth/");
  if (response.ok) {
    const data = await response.json();
    if (data.errors) {
      return;
    }

    dispatch(setUser(data));
  }
};

export const thunkLogin = (credentials) => async (dispatch) => {
  const response = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(credentials),
  });

  if (response.ok) {
    const data = await response.json();
    dispatch(setUser(data));
    return data;
  } else if (response.status < 500) {
    const errorMessages = await response.json();
    console.error(errorMessages);
    return errorMessages;
  } else {
    return { server: "Something went wrong. Please try again" };
  }
};

export const thunkSignup = (user) => async (dispatch) => {
  const response = await fetch("/api/auth/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(user),
  });

  if (response.ok) {
    const data = await response.json();
    dispatch(setUser(data));
  } else if (response.status < 500) {
    const errorMessages = await response.json();
    return errorMessages;
  } else {
    return { server: "Something went wrong. Please try again" };
  }
};

export const thunkLogout = () => async (dispatch) => {
  await fetch("/api/auth/logout");
  dispatch(removeUser());
};

export const getClient = (clientData) => async (dispatch) => {
  const exists = await jsonPost("/clients/exists", clientData)
  dispatch(setClient(exists));
  return exists;
};
export const postClient = (clientData) => async (dispatch) => {
  const exists = await post("/clients", clientData);
  dispatch(setClient(exists));
  return exists;
};
export const deleteClient = () => async (dispatch, getState) => {
  const state = getState()
  const exists = await del("/clients/" + Number(state.session.client.id));
  dispatch(removeClient());
  return exists;
};

const initialState = { user: null, client: null };

function sessionReducer(state = initialState, action) {
  switch (action.type) {
    case SET_USER:
      return { ...state, user: action.payload };
    case REMOVE_USER:
      return { ...state, user: null };
    case SET_CLIENT:
      return { ...state, client: action.client };
    case REMOVE_CLIENT:
      return { ...state, client: null };
    default:
      return state;
  }
}

export default sessionReducer;
