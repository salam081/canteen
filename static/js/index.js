let OrderArray = [];
let mealArray = [
  {
    title: "Pounded-yam",
    url: "/static/img/menu-1.jpg",
    price: 200,
    category: "swallow",
    available: false,
  },
  {
    title: "Jollof-rice",
    url: "/static/img/menu-2.jpg",
    price: 1000,
    category: "normal food",
    available: true,
  },
  {
    title: "Eba",
    url: "/static/img/menu-3.jpg",
    price: 500,
    category: "swallow",
    available: false,
  },
  {
    title: "Coca-Cola",
    url: "/static/img/menu-4.jpg",
    price: 400,
    category: "drink",
    available: true,
  },
  {
    title: "Fanta",
    url: "/static/img/menu-5.jpg",
    price: 900,
    category: "drink",
    available: false,
  },
];

// MEALS
let menuDivs = document.getElementsByClassName("menu");
if (menuDivs.length > 0) {
  let menuDiv = menuDivs[0];

  mealArray.forEach((meal) => {
    let mealDiv = document.createElement("div");
    mealDiv.className = "col-12";
    mealDiv.innerHTML = `<div class="meal d-flex align-items-center" style="cursor: pointer" data-title=${
      meal.title
    }
    data-price=${meal.price}
    data-category=${meal.category}
    data-url=${meal.url}>
    <img
    class="flex-shrink-0 img-fluid rounded"
    src="${meal.url}"
    alt=""
    style="width: 80px"
    />
    <div class="w-100 d-flex flex-column text-start ps-4">
    <h5 class="d-flex justify-content-between border-bottom pb-2">
    <span>${meal.title}</span>
    <span class="text-primary">&#8358;${meal.price}</span>
    <span class="text-primary">${
      meal.available === false ? "Unavailable" : "Available"
    }</span>
    </h5>
    </div>
    </div>`;
    menuDiv.appendChild(mealDiv);
  });
} else {
  console.error("No elements with class 'menu' found.");
}

// SWALLOWS
let swallowDivs = document.getElementsByClassName("swallow-div");
if (swallowDivs.length > 0) {
  let swallowDiv = swallowDivs[0];

  let filteredSwallow = mealArray.filter((meal) => meal.category === "swallow");

  filteredSwallow.forEach((swallow) => {
    let swallowDIV = document.createElement("div");
    swallowDIV.className = "col-12";
    swallowDIV.innerHTML = `<div class="meal d-flex align-items-center" style="cursor: pointer" data-title=${
      swallow.title
    }
          data-price=${swallow.price}
          data-category=${swallow.category}
          data-url=${swallow.url}>
        <img
          class="flex-shrink-0 img-fluid rounded"
          src="${swallow.url}"
          alt=""
          style="width: 80px"
        />
        <div class="w-100 d-flex flex-column text-start ps-4">
          <h5 class="d-flex justify-content-between border-bottom pb-2">
            <span>${swallow.title}</span>
            <span class="text-primary">&#8358;${swallow.price}</span>
            <span class="text-primary">${
              swallow.available === false ? "Unavailable" : "Available"
            }</span>
          </h5>
        </div>
      </div>`;
    swallowDiv.appendChild(swallowDIV);
  });
} else {
  console.error("No elements with class 'menu' found.");
}

// DRINKS
let drinkDivs = document.getElementsByClassName("drink-div");
if (drinkDivs.length > 0) {
  let drinkDiv = drinkDivs[0];

  let filteredDrinks = mealArray.filter((meal) => meal.category === "drink");
  filteredDrinks.forEach((drink) => {
    let drinkDIV = document.createElement("div");
    drinkDIV.className = "col-12";
    drinkDIV.innerHTML = `<div class="meal d-flex align-items-center" style="cursor: pointer" data-title=${
      drink.title
    }
          data-price=${drink.price}
          data-category=${drink.category}
          data-url=${drink.url}>
        <img
          class="flex-shrink-0 img-fluid rounded"
          src="${drink.url}"
          alt=""
          style="width: 80px"
        />
        <div class="w-100 d-flex flex-column text-start ps-4">
          <h5 class="d-flex justify-content-between border-bottom pb-2">
            <span>${drink.title}</span>
            <span class="text-primary">&#8358;${drink.price}</span>
            <span class="text-primary">${
              drink.available === false ? "Unavailable" : "Available"
            }</span>
          </h5>
        </div>
      </div>`;
    drinkDiv.appendChild(drinkDIV);
  });
} else {
  console.error("No elements with class 'menu' found.");
}

// SELECTED MEALS EVENT LISTENER
document.querySelectorAll(".meal").forEach((mealElement) => {
  mealElement.addEventListener("click", function (e) {
    let clickedMeal = e.currentTarget;

    let mealDetails = {
      title: clickedMeal.getAttribute("data-title"),
      price: clickedMeal.getAttribute("data-price"),
      category: clickedMeal.getAttribute("data-category"),
      url: clickedMeal.getAttribute("data-url"),
    };

    console.log(mealDetails);
    console.log(mealDetails.price);
    OrderArray.push({ title: mealDetails.title, price: mealDetails.price });
    UpdateOrderList();
    UpdateTotalPrice();
  });
});

// ORDER UPDATER FUNCTION
function UpdateOrderList() {
  const orderList = document.getElementById("order-list");
  orderList.innerHTML = "";
  console.log(OrderArray);
  if (OrderArray && OrderArray.length > 0) {
    OrderArray.forEach((meal, index) => {
      const mealItem = document.createElement("div");
      mealItem.setAttribute(
        "class",
        "meal-item-style d-flex justify-content-between align-items-center pb-2 "
      );
      mealItem.innerHTML = `
      <h5>${meal.title}</h5>
      <span>
      <span class="text-primary">&#8358; ${meal.price}</span>
      <span class="items-button" style="cursor:pointer" data-index="${index}">❌</span>
      </span>
   `;
      document.getElementById("order-list").appendChild(mealItem);
    });

    document.querySelectorAll(".items-button").forEach((button) => {
      button.addEventListener("click", function () {
        const index = this.getAttribute("data-index");
        OrderArray.splice(index, 1);
        UpdateTotalPrice();
        UpdateOrderList();
        console.log(OrderArray);
      });
    });
  } else {
    orderList.innerHTML = `<div style="position: absolute; top: 30%; left: 35%">
            <img src="/static/img/chef.jpeg" alt="chef image" />
            <p><i>Start placing your order...</i></p>
          </div>`;
  }
}

// TOTAL PRICE UPDATER AND DISPLAY
function UpdateTotalPrice() {
  const nairaSign = "\u20A6";
  let totalPrice = OrderArray.reduce(
    (sum, meal) => sum + Number(meal.price),
    0
  );

  document.getElementById(
    "totalDiv"
  ).innerHTML = `<h2 class="text-primary border-top">Total: ${nairaSign} ${totalPrice}</h2>`;
}

//giving nav-links active class
const navLinks = document.querySelectorAll('.nav-link');
console.log(navLinks)
const currentPath = window.location.pathname;
navLinks.forEach(link => {
    if (link.getAttribute('href') === currentPath) {
        link.classList.add('active');
    }
});
