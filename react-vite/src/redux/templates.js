import { createSelector } from "reselect";

import { get, jsonPost, jsonPut, formPost, formPut, del } from "./customFetch";

/* TYPES */

const LOAD_TEMPLATE = "templates/loadTemplate";
const LOAD_TEMPLATES = "templates/loadTemplates";
const REMOVE_TEMPLATE = "templates/removeTemplate";

/* ACTIONS */

const loadOne = (template) => ({
  type: LOAD_TEMPLATE,
  template,
});
const removeOne = (templateId) => ({
  type: REMOVE_TEMPLATE,
  templateId,
});
const loadAll = (templates) => ({
  type: LOAD_TEMPLATES,
  templates,
});

/* THUNKS */

export const fetchTemplate = (templateId) => async (dispatch) => {
  const data = await get(`/templates/${templateId}`);
  dispatch(loadOne(data));
  return data;
};
export const fetchTemplates = () => async (dispatch) => {
  const data = await get(`/templates`);
  dispatch(loadAll(data));
  return data;
};
export const postTemplate = (templateBody) => async (dispatch) => {
  const data = await jsonPost(`/templates`, templateBody);
  dispatch(loadOne(data));
  return data;
};
export const deleteTemplate = (templateId) => async (dispatch) => {
  const data = await del(`/templates/${templateId}`);
  dispatch(removeOne(templateId));
  return data;
};

/* SELECTORS */

export const selectTemplateById = (templateId) => (state) =>
  state.templates[templateId];
export const selectTemplateArray = createSelector(
  [(state) => state.templates],
  (templates) => Object.values(templates)
);
export const selectTemplateByName = createSelector(
  [selectTemplateArray, (state, templateName) => templateName],
  (templates, templateName) =>
    templates.find(({ name }) => name == templateName)
);

/* REDUCER */

const initialState = {};

function templateReducer(state = initialState, action) {
  switch (action.type) {
    case LOAD_TEMPLATE: {
      return { ...state, [action.template.id]: action.template };
    }
    case LOAD_TEMPLATES: {
      return {
        ...state,
        ...action.templates.reduce(
          (obj, temp) => ({ ...obj, [temp.id]: temp }),
          {}
        ),
      };
    }
    case REMOVE_TEMPLATE: {
      const { [action.templateId]: remove, ...rest } = state;
      return rest;
    }
    default:
      return state;
  }
}

export default templateReducer;
