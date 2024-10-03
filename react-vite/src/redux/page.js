import { get, jsonPost, jsonPut, formPost, formPut, del } from "./customFetch";

/* TYPES */

const LOAD_PAGE = "session/loadPage";
const REMOVE_PAGE = "session/removePage";
const EDIT_PAGE = "session/editPage";

const LOAD_CONTENT = "session/loadContent";
const EDIT_CONTENT = "session/editContent";
const DELETE_CONTENT = "session/deleteContent";

/* ACTIONS */

const loadOne = (page) => ({
  type: LOAD_PAGE,
  page,
});
const loadContent = (pageId, content) => ({
  type: LOAD_CONTENT,
  pageId,
  content,
});
const editPage = (page) => ({
  type: EDIT_PAGE,
  page,
});
const unloadOne = (pageId) => ({
  type: REMOVE_PAGE,
  pageId,
});
const editContent = (content) => ({
  type: EDIT_CONTENT,
  content,
});
const removeContent = (contentId) => ({
  type: LOAD_CONTENT,
  contentId,
});

/* THUNKS */

export const fetchPage = (pageId) => async (dispatch) => {
  const data = await get(`/pages/${pageId}`);
  dispatch(loadOne(data));
  return data;
};
export const postPage = (pageData) => async (dispatch) => {
  const data = await jsonPost(`/pages`, pageData);
  dispatch(loadOne(data));
  return data;
};
export const putPage = (pageData) => async (dispatch) => {
  const data = await jsonPut(`/pages`, pageData);
  dispatch(editPage(data));
  return data;
};
export const deletePage = (pageId) => async (dispatch) => {
  const data = await del(`/pages`, pageId);
  dispatch(unloadOne(pageId));
  return data;
};
export const postContent = (pageId, content) => async (dispatch) => {
  const data = await formPost(`/content`, { ...content, pageId });
  dispatch(loadContent(data));
  return data;
};
export const putContent = (content) => async (dispatch) => {
  const data = await formPut(`/content${content.id}`, content);
  dispatch(editContent(data));
  return data;
};
export const deleteContent = (contentId) => async (dispatch) => {
  const data = await del(`/content${contentId}`);
  dispatch(removeContent(contentId));
  return data;
};
export const publishPage = (pageId) => async (dispatch) => {
  const data = await jsonPost(`/pages/${pageId}/publish`);
  dispatch(loadOne(data));
  return data;
};
export const unpublishPage = (pageId) => async (dispatch) => {
  const data = await jsonPost(`/pages/${pageId}/unpublish`);
  dispatch(loadOne(data));
  return data;
};

/* SELECTORS */

export const selectPageById = (pageId) => (state) => state.pages[pageId];
export const selectPageContentByPageId = (pageId) => (state) =>
  state.pages[pageId]?.content;

/* REDUCER */

const initialState = {};

function pageReducer(state = initialState, action) {
  switch (action.type) {
    case EDIT_PAGE:
    case LOAD_PAGE:
      return { ...state, [action.page.id]: action.page };
    case REMOVE_PAGE: {
      const { pageId } = action;
      const { [pageId]: rest, ...newState } = state;
      return newState;
    }
    case LOAD_CONTENT: {
      const { pageId, content } = action;
      const page = state[pageId];
      return {
        ...state,
        [pageId]: {
          ...page,
          content: [...page.content, content],
        },
      };
    }
    case DELETE_CONTENT: {
      const { contentId } = action;
      const pageId = Number(contentId.split("_")[0]);
      const page = state[pageId];
      return {
        ...state,
        [pageId]: {
          ...page,
          content: page.content.filter(({ id }) => id != contentId),
        },
      };
    }
    case EDIT_CONTENT: {
      const { content } = action;
      const contentId = content.id;
      const pageId = Number(contentId.split("_")[0]);
      const page = state[pageId];
      return {
        ...state,
        [pageId]: {
          ...page,
          content: page.content.map((cont) =>
            cont.id == contentId ? content : cont
          ),
        },
      };
    }
    default:
      return state;
  }
}

export default pageReducer;
