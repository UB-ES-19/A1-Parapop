function admSelectCheck(nameSelect){
    if(nameSelect.value == "Todo"){
      document.getElementById("PrecioIni").style.display = "none";
      document.getElementById("PrecioFi").style.display = "none";
      document.getElementById("Localizacion").style.display = "none";
      document.getElementById("filtro_loc").style.display = "none";
      document.getElementById("filtro_precio").style.display = "none";
    }

    if(nameSelect.value == "Precio"){
      document.getElementById("PrecioIni").style.display = "inline";
      document.getElementById("PrecioFi").style.display = "inline";
      document.getElementById("Localizacion").style.display = "none";
      document.getElementById("filtro_loc").style.display = "none";
      document.getElementById("filtro_precio").style.display = "inline";
    }

    if(nameSelect.value == "Ciudad"){
      document.getElementById("PrecioIni").style.display = "none";
      document.getElementById("PrecioFi").style.display = "none";
      document.getElementById("Localizacion").style.display = "inline";
      document.getElementById("filtro_loc").style.display = "inline";
      document.getElementById("filtro_precio").style.display = "none";
    }

    if(nameSelect.value == "Hora"){
      document.getElementById("PrecioIni").style.display = "none";
      document.getElementById("PrecioFi").style.display = "none";
      document.getElementById("Localizacion").style.display = "none";
      document.getElementById("filtro_loc").style.display = "none";
      document.getElementById("filtro_precio").style.display = "none";
    }

}
window.onload = function(){
    document.getElementById('getFname').onchange();
}
