// here all the code that connect the html view to the server.

$(document).ready(
    function() {
    let array_to_send = []
    let shift_percentage = []
    let selected_algo = []
    function CreateTable(name){
        let table = document.createElement("TABLE")
        table.border = ""
        table.width = "50%"
        let thead = table.createTHead();
        let row = thead.insertRow(0)
        let table_head_cells = []
        let j = 0;
        for (j = 0; j < 2; j++){
            table_head_cells[j] = row.insertCell(j)
        }
        table_head_cells[0].innerHTML = "M"
        table_head_cells[1].innerHTML = "N"

        let tbody_row = table.insertRow(1)
        let input_cells = []
        for (j = 0; j < 2; j++){
            input_cells[j] = document.createElement("INPUT");
            input_cells[j].setAttribute("type", "checkbox");
            input_cells[j].addEventListener("change",function () {
                let bartender = $(this).closest('table').closest('tr')[0].rowIndex - 1
                let day = $(this).closest('table').closest('td')[0].cellIndex - 2
                let shift = $(this).closest('td')[0].cellIndex
                let weekly_shift = array_to_send[bartender].split(" ")
                let temp_shift = ""
                let daily_shift = "1"
                if (this.checked) {
                    daily_shift = "0"
                }
                weekly_shift[day].split('').forEach(function (val, index) {
                    if (index === shift){
                        temp_shift += daily_shift
                    }else {
                        temp_shift += val
                    }
                })
                weekly_shift[day] = temp_shift
                array_to_send[bartender] = weekly_shift.join(' ')  // update the shifts of the bartender
            })
            tbody_row.insertCell(j).appendChild(input_cells[j])
        }
        return table;
    }

    function create_new_bartender() {
        array_to_send.push("11 11 11 11 11")
        let bartender_table = document.getElementById("bartender_table_body")
        let row = bartender_table.insertRow(bartender_table.rows.length)
        let i = 0;
        let input_cell = []
        input_cell[0] = document.createElement("INPUT");
        input_cell[0].setAttribute("type", "text");
        input_cell[1] = document.createElement("INPUT");
        input_cell[1].setAttribute("type", "text");
        let cells = [];
        for (i = 0; i < 7; i++) {
            cells[i] = row.insertCell(i);
            if (i === 0 || i === 1) {
                cells[i].appendChild(input_cell[i])
            } else {
                cells[i].appendChild(CreateTable())
            }
        }
        return row;
    }
    function get_bartender_names() {
        let names = []
        for (let row of document.getElementById("bartender_table_body").rows) {
            names.push(row.cells[0].children[0].value)
        }
        return names
    }
    function build_result_table(shifts) {
        let shifts_dic = {"0":"M", "1":"N"}
        let days_dic = {"1": "ST", "2":"MT", "3":"TT", "4":"WT", "5":"ThT"}
        Object.keys(shifts_dic).forEach(function (shift_key_val) {
            Object.keys(days_dic).forEach(function (day_key) {
                $("#" + shifts_dic[shift_key_val] + days_dic[day_key]).empty()
            })
        })
        if (shifts[0] !== "there is no solution!") {
            let names = get_bartender_names()
            let day = ""
            shifts.forEach(function (bartender_shift, index) {
                bartender_shift = bartender_shift.trim()
                if (bartender_shift === ""){
                    return;
                }
                let split_n = bartender_shift.split(" ")
                if (split_n[0] === "Day"){
                    day = split_n[1]
                } else {
                    let table = document.getElementById(shifts_dic[split_n[4]] + days_dic[day])
                    let row = table.insertRow(table.rows.length)
                    let x = document.createElement("LABEL");
                    x.innerHTML = names[split_n[1]]
                    let cell = row.insertCell(0)
                    cell.appendChild(x);
                    if (split_n.length === 5) {
                        cell.style.background = "#FFFF00"
                    } else {
                        cell.style.background = "#FF6347"
                    }
                }
            })
        }
    }
    function GetData(result) {
        $.ajax({
            type: 'GET',
            contentType: 'application/json',
            url: '/get_data',
            dataType: 'json',
            success: function (result) {
                present_data(result)
            }, error: function (result) {
                present_data(result)
            }
        });
        $("#result_div").slideDown("slow");
        $("#image_div").slideDown("slow");
        if (selected_algo[0] === "simulated_annealing" || selected_algo[0] === "genetic" ||
            selected_algo[0] === "hill_climbing" || selected_algo[0] === "random_restart") {
            let d = new Date()
            $("#graph_image").attr("src", "/static/OptimizationGui.png?"+d.getTime());
            let img = document.getElementById("graph_image");
            img.style.display = "flex";
        }
        document.getElementById("backdrop").style.visibility = "hidden"
        document.getElementById("curtain").style.visibility = "visible"
        build_result_table(result)
    }
    function present_data(data){
        if (data.status === 200) {
            document.getElementById("backdrop").style.visibility = "hidden"
            document.getElementById("curtain").style.visibility = "visible"
            $("#curtain").html(data.responseText);
        }
    }
    document.getElementById("start").addEventListener("click",function () {
        if (array_to_send.length === 0){
            alert("Please Insert Bartender Input")
            return;
        }
        shift_percentage = []
        for (let row of document.getElementById("bartender_table_body").rows) {
            if (row.cells[1].children[0].value === "") {
                alert("Please enter percentage shift for each bartender")
                return
            } else {
                shift_percentage.push(row.cells[1].children[0].value)
            }
        }
        if (selected_algo.length === 0) {
            alert("Please Select Algorithm!")
            return;
        }
        if ($("#" + selected_algo[0] + "_txt").length) {
            let algo_parameter = document.getElementById(selected_algo[0] + "_txt").value
            if (algo_parameter === "") {
                alert("Please define the algorithm parameter!")
                return;
            } else {
                if (selected_algo.length === 2) {
                    let algo_name = selected_algo[0]
                    selected_algo = []
                    selected_algo.push(algo_name)
                }
                selected_algo.push(algo_parameter)
            }
        }
        let data = []
        data.push(array_to_send)
        data.push(shift_percentage)
        data.push(selected_algo)
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/user_data',
            dataType: 'json',
            data: JSON.stringify(data),
            success: function (result) {
                GetData(result);
            }, error: function (result) {
                GetData(result);
            }
        });
    })
    document.getElementById("insert_new_bartender").addEventListener("click",create_new_bartender)
    document.getElementById("generate_random").addEventListener("click",function () {
        array_to_send = []
        let num_bartender = parseInt(document.getElementById("num_bartender").value)
        if (isNaN(num_bartender)){
            alert("choose number of bartenders")
            return
        } else if (num_bartender < 0){
            alert("The number of the bartenders can not be negative")
            return;
        }
        $("#bartender_table_body").empty()
        let bartender_num = num_bartender
        while(num_bartender > 0){
            let row = create_new_bartender()
            let i = 0;
            let j = 0;
            for(i = 0; i < row.cells.length;i++){
                if (row.cells[i].children[0].tagName === "TABLE"){
                    let table = row.cells[i].children[0]
                    for (j = 0; j < table.rows[1].cells.length; j++){
                        if (Math.random() >= 0.5){
                            table.rows[1].cells[j].children[0].checked = true
                            table.rows[1].cells[j].children[0].dispatchEvent(new Event("change"))
                        }
                    }
                } else {
                    if (i !== 1) {
                        row.cells[i].children[0].value = "Bartender" + (bartender_num - num_bartender + 1).toString()
                    } else {
                        row.cells[i].children[0].value = Math.floor(Math.random() * 4) + 2
                    }
                }
            }
            num_bartender = num_bartender - 1;
        }
    })

    let check_box_ids = ["shift_min","simulated_annealing","genetic","random_restart", "hill_climbing", "csp", "MaxShifts"]
    let check_box_item = []
    check_box_ids.forEach(function (check_box_id) {
        let c_item = document.getElementById(check_box_id)
        c_item.addEventListener("change",function () {
            let item_change = this
            if (selected_algo.length > 0) {
                selected_algo = []
            }
            if (item_change.checked) {
                if ($("#" + item_change.id + "_div").length) {
                    $("#" + item_change.id + "_div").slideDown("slow");
                }
                selected_algo.push(item_change.id)
                check_box_item.forEach(function (item_value) {
                    if (item_change !== item_value) {
                        if (item_value.checked) {
                            item_value.checked = false;
                        }
                        if ($("#" + item_value.id + "_div").length) {
                            let txt_input = document.getElementById(item_value.id + "_txt")
                            txt_input.value = ""
                            $("#" + item_value.id + "_div").slideUp("slow");
                        }
                    }
                })
            } else {
                if ($("#" + item_change.id + "_txt").length) {
                    $("#" + item_change.id + "_div").slideUp("slow");
                }
            }
        })
        check_box_item.push(c_item)
    })
})