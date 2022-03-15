import { API } from "../../backend";

// set the cart in localstorage if it is not already there
if (!localStorage.getItem("cart")) {
  localStorage.setItem("cart", JSON.stringify([]));
}

// get the list of products from the backend.
export const getProducts = () => {
  return fetch(`${API}product`, { method: "GET" })
    .then((response) => {
      return response.json();
    })
    .catch((err) => console.log(err));
};
