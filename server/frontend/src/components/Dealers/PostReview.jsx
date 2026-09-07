import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "./Dealers.css";
import "../assets/style.css";
import Header from "../Header/Header";

const PostReview = () => {
  const { id } = useParams();

  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState("");
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);

  const postreview = async () => {
    let name =
      sessionStorage.getItem("firstname") +
      " " +
      sessionStorage.getItem("lastname");

    if (!name || name.includes("null")) {
      name = sessionStorage.getItem("username") || "testuser";
    }

    if (!model || !review || !date || !year) {
      alert("All details are mandatory");
      return;
    }

    const [car_make, ...modelParts] = model.split("|");
    const car_model = modelParts.join("|");

    const res = await fetch("/djangoapp/add_review", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name,
        dealership: Number(id),
        review,
        purchase: true,
        purchase_date: date,
        car_make,
        car_model,
        car_year: Number(year),
      }),
    });

    const json = await res.json();

    if (json.status === 200) {
      window.location.href = `/dealer/${id}`;
    } else {
      alert("Unable to post review");
    }
  };

  const getDealer = async () => {
    const res = await fetch(`/djangoapp/dealer/${id}`);
    const data = await res.json();
    setDealer(data);
  };

  const getCars = async () => {
    const res = await fetch("/djangoapp/get_cars");
    const data = await res.json();

    const cars = [];
    data.forEach((make) => {
      make.models.forEach((car) => {
        cars.push({
          make: make.make,
          model: car.name,
          year: car.year,
        });
      });
    });

    setCarmodels(cars);
  };

  useEffect(() => {
    getDealer();
    getCars();
  }, [id]);

  return (
    <div>
      <Header />

      <div style={{ margin: "5%" }}>
        <h1 style={{ color: "darkblue" }}>
          Review Dealer: {dealer.full_name}
        </h1>

        <div className="input_field">
          <textarea
            id="review"
            cols="50"
            rows="7"
            placeholder="Write your review"
            value={review}
            onChange={(e) => setReview(e.target.value)}
          />
        </div>

        <div className="input_field">
          Purchase Date{" "}
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </div>

        <div className="input_field">
          Car Make and Model{" "}
          <select
            name="cars"
            id="cars"
            value={model}
            onChange={(e) => setModel(e.target.value)}
          >
            <option value="" disabled>
              Choose Car Make and Model
            </option>

            {carmodels.map((car, index) => (
              <option
                key={index}
                value={`${car.make}|${car.model}`}
              >
                {car.make} {car.model}
              </option>
            ))}
          </select>
        </div>

        <div className="input_field">
          Car Year{" "}
          <input
            type="number"
            value={year}
            onChange={(e) => setYear(e.target.value)}
            max="2023"
            min="2015"
          />
        </div>

        <div>
          <button className="postreview" onClick={postreview}>
            Post Review
          </button>
        </div>
      </div>
    </div>
  );
};

export default PostReview;
