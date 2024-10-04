import { createSelector } from "reselect";
import { get, jsonPost, jsonPut, formPost, formPut, del } from "./customFetch";

/* TYPES */

const LOAD_WORKSHOP_TYPE = "workshops/loadWorkshopType";
const LOAD_WORKSHOP_TYPES = "workshops/loadWorkshopTypes";
const LOAD_WORKSHOP = "workshops/loadWorkshops";

/* ACTIONS */

const loadOne = (workshopType) => ({
  type: LOAD_WORKSHOP_TYPE,
  workshopType,
});
const loadAll = (workshopTypes) => ({
  type: LOAD_WORKSHOP_TYPES,
  workshopTypes,
});
const loadWorkshop = (workshop) => ({
  type: LOAD_WORKSHOP,
  workshop,
});

/* THUNKS */

export const fetchWorkshopType = (workshopTypeId) => async (dispatch) => {
  const data = await get(`/workshopTypes/${workshopTypeId}`);
  dispatch(loadOne(data));
  return data;
};
export const fetchWorkshopTypes = () => async (dispatch) => {
  const data = await get(`/workshopTypes`);
  dispatch(loadAll(data));
  return data;
};
export const postWorkshop = (workshopBody) => async (dispatch) => {
  const data = await jsonPost(`/workshops`, workshopBody);
  dispatch(loadWorkshop(data));
  return data;
};

/* SELECTORS */

export const selectWorkshopTypeById = (workshopTypeId) => (state) =>
  state.workshopTypes[workshopTypeId];
export const selectWorkshopTypeByName = (workshopTypeName) => (state) =>
  state.workshopTypes[state.types[workshopTypeName]];
export const selectWorkshopTypesArray = (state) => state.workshopTypes.types;

/* REDUCER */

const initialState = { types: [] };

function workshopTypeReducer(state = initialState, action) {
  switch (action.type) {
    case LOAD_WORKSHOP_TYPE:
      const types = state.types;

      return {
        ...state,
        [action.workshopType.id]: action.workshopType,
        types: [
          ...types.filter(({ id }) => id != action.workshopType.id),
          action.workshopType,
        ],
      };
    case LOAD_WORKSHOP_TYPES:
      return {
        ...state,
        ...action.workshopTypes.reduce(
          (obj, type) => ({ ...obj, [type.id]: type }),
          {}
        ),
        types: action.workshopTypes,
      };
    case LOAD_WORKSHOP: {
      const typeId = action.workshop.workshopTypeId;
      const oldWorkshop = state[typeId];
      const newWorkshop = {
        ...oldWorkshop,
        workshops: [...oldWorkshop.workshops, action.workshop],
      };
      return {
        ...state,
        [typeId]: newWorkshop,
        types: state.types.map((ele) => (ele.id == typeId ? newWorkshop : ele)),
      };
    }
    default:
      return state;
  }
}

export default workshopTypeReducer;
