import { API } from "../../backend";

if (!localStorage.getItem("cart")) {
  localStorage.setItem("cart", JSON.stringify([]));
}

export const getProducts = () => {
  // get the list of products from the backend.
  return fetch(`${API}product`, { method: "GET" })
    .then((response) => {
      return response.json();
    })
    .catch((err) => console.log(err));
};
