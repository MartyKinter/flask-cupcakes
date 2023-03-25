const BASE_URL = "http://127.0.0.1:5000/api";

//creates html for cupcakes in database
function generateCupcakeHTML(cupcake){
    return `
    <div data-cupcake-id=${cupcake.id} class="col-3">
        <li>
        ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
        <button class="delete-button btn-danger btn-sm">X</button>
        </li>
        <img class="Cupcake-img"
            src="${cupcake.image}"
            alt="(no image provided)">
    </div>`;
}

//displays cupcakes in database on start
async function showInitialCupcakes(){
    const response = await axios.get(`${BASE_URL}/cupcakes`);

    for (let cupcakeData of response.data.cupcakes){
        let newCupcake = $(generateCupcakeHTML(cupcakeData));
        $("#cupcakes-list").append(newCupcake);
    }
}

//handles submitting new cupcake form
$("#new-cupcake-form").on("submit", async function (evt){
    evt.preventDefault();

    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val();

    const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor,
        rating,
        size,
        image
    });
    let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
    $("#cupcakes-list").append(newCupcake);
    $("#new-cupcake-form").trigger("reset");
});

//handles deleting a cupcake when button is pushed
$("#cupcakes-list").on("click", ".delete-button", async function(evt){
    evt.preventDefault();
    let $cupcake = $(evt.target). closest("div");
    let cupcakeId = $cupcake.attr("data-cupcake-id");

    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
});

$(showInitialCupcakes);