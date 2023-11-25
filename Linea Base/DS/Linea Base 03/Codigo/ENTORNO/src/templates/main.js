// Datos para el primer gráfico
const chartData1 = {
  labels: ["Active", "Inactive", "Disabled"],
  data: [60, 30, 10],
};

const myChart1 = document.getElementById("grafico-circular-1");
const ul1 = document.querySelector(".section-1 .grafico-elementos ul");

new Chart(myChart1, {
  type: "doughnut",
  data: {
    labels: chartData1.labels,
    datasets: [
      {
        label: "Denuncias",
        data: chartData1.data,
        backgroundColor: [
          "#2196F3",
          "#FFC107",
          "#023047",
        ],
      },
    ],
  },
  options: {
    borderWidth: 10,
    borderRadius: 2,
    hoverBorderWidth: 0,
    plugins: {
      legend: {
        display: false,
      },
    },
  },
});

const populateUl1 = () => {
  chartData1.labels.forEach((l, i) => {
    let li = document.createElement("li");
    li.innerHTML = `${l}: <span class='porcentaje'>${chartData1.data[i]}%</span>`;
    ul1.appendChild(li);
  });
};

populateUl1();

// Datos para el segundo gráfico
const chartData2 = {
  labels: ["07/10/23", "08/10/23","09/10/23", "10/10/23", "11/10/23"],
  data: [30, 40, 20,25, 35, 18],
};

const myChart2 = document.getElementById("grafico-barras-2");
const ul2 = document.querySelector(".section-2 .grafico-elementos ul");

new Chart(myChart2, {
  type: "bar",
  data: {
    labels: chartData2.labels,
    datasets: [
      {
        label: "Denuncias",
        data: chartData2.data,
        backgroundColor: [
          "#FF5733",
          "#4CAF50",
          "#9C27B0",
          "#FF9800",
          "#E91E63",
        ],
      },
    ],
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
        max: 50,
      },
    },
    plugins: {
      legend: {
        display: false,
      },
    },
  },
});

const populateUl2 = () => {
  chartData2.labels.forEach((l, i) => {
    let li = document.createElement("li");
    li.innerHTML = `${l}: <span class='porcentaje'>${chartData2.data[i]}%</span>`;
    ul2.appendChild(li);
  });
};

populateUl2();

// Agrega un controlador de eventos al campo de búsqueda
const searchInput = document.getElementById('search');
searchInput.addEventListener('input', function () {
    // Obtén el término de búsqueda y conviértelo a minúsculas
    const searchTerm = searchInput.value.toLowerCase();

    // Obtén todas las filas de la tabla
    const filas = document.querySelectorAll('.fila');

    // Itera a través de las filas
    filas.forEach(function (fila) {
        // Obtiene el contenido de la columna "Categoria" y conviértelo a minúsculas
        const categoria = fila.querySelector('.categoria').textContent.toLowerCase();

        // Realiza la búsqueda en la columna "Categoria"
        if (categoria.includes(searchTerm)) {
            fila.style.display = 'block';
        } else {
            fila.style.display = 'none';
        }
    });
});
