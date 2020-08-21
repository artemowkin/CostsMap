let month_graph = document.getElementById('statistic_graph').getContext('2d');
let year_graph = document.getElementById('year_statistic_graph').getContext('2d')

function set_canvas_width(context) {
    if (document.documentElement.clientWidth > 1024) {
        context.canvas.width = 500;
        context.canvas.height = 500;
    } else {
        context.canvas.width = 300;
        context.canvas.height = 300;
    }
}

function create_month_graph(data, context) {
    let categories = [];
    let costs = [];

    set_canvas_width(context)

    for (let stat of data) {
        categories.push(stat.category);
        costs.push(stat.costs);
    }

    let chart = new Chart(context, {
        type: 'pie',
        data: {
            labels: categories,
            datasets: [{
                label: 'Costs',
                data: costs,
                backgroundColor: "#333",
            }],
        },
        options: {
            title: {
                display: true,
                text: 'Costs for each category per month'
            },
            responsive: false
        }
    })
}

function create_year_graph(data, context) {
    let months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ];
    let costs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

    set_canvas_width(context);

    for (let stat of data) {
        costs[stat.cost_month-1] = stat.cost_sum;
    }

    let chart = new Chart(context, {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: 'Costs',
                data: costs,
                backgroundColor: "#333",
            }],
        },
        options: {
            title: {
                display: true,
                text: 'Costs by months for the last year'
            },
            responsive: false
        }
    })
}

async function get_month_data() {
    let current_date = document.querySelector('.dates_current_date');
    let date_string = current_date.textContent.trim();
    let url = `/costs/${date_string}/statistic/json/`;
    let response = await fetch(url);
    let json = await response.json();
    return json;
}

async function get_year_data() {
    let current_date = document.querySelector('.dates_current_date');
    let year_string = current_date.textContent.trim().slice(0, 4);
    let url = `/costs/${year_string}/statistic/json/`;
    let response = await fetch(url);
    let json = await response.json();
    return json;
}

get_month_data().then(data => create_month_graph(data, month_graph));
get_year_data().then(data => create_year_graph(data, year_graph))

