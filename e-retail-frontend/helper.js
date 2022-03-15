import { API } from "../../backend";

import { cartEmpty } from "../../core/helper/cartHelper";

// function for handling sign-up
export const signup = (user) => {
  return fetch(`${API}user/`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(user),
  })
    .then((response) => {
      return response.json();
    })
    .catch((err) => console.log(err));
};

// function handling sign-in
export const signin = (user) => {
  const formData = new FormData();

  for (const name in user) {
    formData.append(name, user[name]);
  }

  return fetch(`${API}user/login/`, {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      return response.json();
    })
    .catch((err) => console.log(err));
};

// authenticates the user
export const authenticate = (data, next) => {
  if (typeof window !== undefined) {
    localStorage.setItem("token", JSON.stringify(data));
    next();
  }
};

// check if a user is authenticated or not.
export const isAuthenticated = () => {
  if (typeof window == undefined) {
    return false;
  }
  if (localStorage.getItem("token")) {
    return JSON.parse(localStorage.getItem("token"));
  } else {
    return false;
  }
};

// sign a user out
export const signout = (next) => {
  const userId = isAuthenticated() && isAuthenticated().user.id;

  if (typeof window !== undefined) {
    localStorage.removeItem("name");
    localStorage.removeItem("token");
    cartEmpty(() => {});
    next();

    return fetch(`${API}user/logout/${userId}`, {
      mathod: "GET",
    })
      .then((response) => {
        next();
      })
      .catch((err) => console.log(err));
  }
};
