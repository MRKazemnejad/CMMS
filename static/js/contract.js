function contractType() {
    var value = document.getElementById('contracttype').value;

    if (value == 1) {
        document.getElementById('system').style.display = 'none';
        document.getElementById('part').style.display = 'none';

        document.getElementById('contract_price1').style.display = '';
        document.getElementById('contract_price2').style.display='none';
        document.getElementById('contract_price3').style.display='none';
        document.getElementById('contract_price4').style.display='none';
        document.getElementById('con_price_sel_display').style.display = 'none';
        document.getElementById('Pre_pay_display').style.display = '';



    } else if (value == 2) {
        document.getElementById('system').style.display = '';
        document.getElementById('part').style.display = '';
        document.getElementById('contract_price1').style.display = '';
        document.getElementById('contract_price2').style.display='none';
        document.getElementById('contract_price3').style.display='none';
        document.getElementById('contract_price4').style.display='none';
        document.getElementById('con_price_sel_display').style.display = 'none';
        document.getElementById('Pre_pay_display').style.display = '';

    } else if (value == 3) {
        document.getElementById('system').style.display = '';
        document.getElementById('part').style.display = '';

        document.getElementById('con_price_sel_display').style.display = '';
        document.getElementById('contract_price1').style.display = 'none';
         document.getElementById('contract_price2').style.display='none';
        document.getElementById('contract_price3').style.display='none';
        document.getElementById('contract_price4').style.display='none';
        const selectedElement=document.getElementById('con_price_sel');
        selectedElement.selectedIndex=0;


    } else if (value == 4) {
        document.getElementById('system').style.display = '';
        document.getElementById('part').style.display = '';
        document.getElementById('contract_price1').style.display = '';
        document.getElementById('contract_price2').style.display='none';
        document.getElementById('contract_price3').style.display='none';
        document.getElementById('contract_price4').style.display='none';
        document.getElementById('con_price_sel_display').style.display = 'none';
        document.getElementById('Pre_pay_display').style.display = '';

    } else if (value == 5) {
        document.getElementById('system').style.display = '';
        document.getElementById('part').style.display = '';
        document.getElementById('contract_price1').style.display = '';
        document.getElementById('contract_price2').style.display='none';
        document.getElementById('contract_price3').style.display='none';
        document.getElementById('contract_price4').style.display='none';
        document.getElementById('con_price_sel_display').style.display = 'none';
        document.getElementById('Pre_pay_display').style.display = '';

    } else if (value == 6) {
        document.getElementById('system').style.display = '';
        document.getElementById('part').style.display = '';
        document.getElementById('contract_price1').style.display = '';
        document.getElementById('contract_price2').style.display='none';
        document.getElementById('contract_price3').style.display='none';
        document.getElementById('contract_price4').style.display='none';
        document.getElementById('con_price_sel_display').style.display = 'none';
        document.getElementById('Pre_pay_display').style.display = '';
    } else if (value == 7) {
        document.getElementById('system').style.display = '';
        document.getElementById('part').style.display = '';
        document.getElementById('contract_price1').style.display = '';
        document.getElementById('contract_price2').style.display='none';
        document.getElementById('contract_price3').style.display='none';
        document.getElementById('contract_price4').style.display='none';
        document.getElementById('con_price_sel_display').style.display = 'none';
        document.getElementById('Pre_pay_display').style.display = '';
    }else if(value == 0){
         document.getElementById('contract_price1').style.display = 'none';
        document.getElementById('contract_price2').style.display='none';
        document.getElementById('contract_price3').style.display='none';
        document.getElementById('contract_price4').style.display='none';
        document.getElementById('con_price_sel_display').style.display = 'none';
        document.getElementById('Pre_pay_display').style.display = 'none';

    }

}

// **************************************************************************************************************
function showpricefield() {

    var value = document.getElementById("customSwitch1").checked;

    if (value == true) {

        document.getElementById("prepayment").disabled = false;
    } else {
        document.getElementById("prepayment").disabled = true;
    }
}

// ****************************************************************************************************************
function precheck1() {
    var value = document.getElementById("customCheck1").checked;
    if (value == true) {

        document.getElementById("presentcheck1").disabled = false;
    } else {
        document.getElementById("presentcheck1").disabled = true;
    }
}

function precheck2() {
    var value = document.getElementById("customCheck2").checked;
    if (value == true) {

        document.getElementById("presentcheck2").disabled = false;
    } else {
        document.getElementById("presentcheck2").disabled = true;
    }
}

function precheck3() {
    var value = document.getElementById("customCheck3").checked;
    if (value == true) {

        document.getElementById("presentcheck3").disabled = false;
    } else {
        document.getElementById("presentcheck3").disabled = true;
    }
}

// ********************************************************************************************************************
function filecheck1() {
    var value = document.getElementById("customCheck4").checked;
    if (value == true) {

        document.getElementById("Commissioncode").disabled = false;
        document.getElementById("Commissionfile").disabled = false;
    } else {
        document.getElementById("Commissioncode").disabled = true;
        document.getElementById("Commissionfile").disabled = true;
    }
}

function filecheck2() {
    var value = document.getElementById("customCheck5").checked;
    if (value == true) {

        document.getElementById("approvalcode").disabled = false;
        document.getElementById("approvalfile").disabled = false;
    } else {
        document.getElementById("approvalcode").disabled = true;
        document.getElementById("approvalfile").disabled = true;
    }
}

function filecheck3() {
    var value = document.getElementById("customCheck6").checked;
    if (value == true) {

        document.getElementById("contractcode1").disabled = false;
        document.getElementById("contractfile").disabled = false;
    } else {
        document.getElementById("contractcode1").disabled = true;
        document.getElementById("contractfile").disabled = true;
    }
}

function filecheck4() {
    var value = document.getElementById("customCheck7").checked;
    if (value == true) {

        document.getElementById("Ceopermissioncode").disabled = false;
        document.getElementById("Ceopermissionfile").disabled = false;
    } else {
        document.getElementById("Ceopermissioncode").disabled = true;
        document.getElementById("Ceopermissionfile").disabled = true;
    }
}

// ********************************************************************************************************************
function contractextensiondetails() {

    document.getElementById("contractshow1").style.display = '';
    document.getElementById("contractshow2").style.display = '';
    document.getElementById("contractshow3").style.display = '';
    document.getElementById("contractshow4").style.display = '';

}

// ************************************************************************************************************************

function getcontractdata(id) {

    var value = id;

    $.ajax({
        url: "/contractDashboard/contractGetData",
        data: {
            'message': JSON.stringify(value),
        },
        success: function (data) {
            document.getElementById('contract_title').value = data.contractdata.contract_title;
            document.getElementById('contractor').value = data.contractdata.contract_contractor;
            document.getElementById('contract_type').value = data.contractdata.contract_type;
            document.getElementById('startdate').value = data.contractdata.contract_startdate;
            document.getElementById('project_name').value = data.contractdata.contract_projectname;
            document.getElementById('contract_code1').value = data.contractdata.contract_code;
            document.getElementById('contract_priode').value = data.contractdata.contract_period;
            document.getElementById('enddate').value = data.contractdata.contract_enddate;
            document.getElementById('warranty').value = data.contractdata.contract_warranty;
            document.getElementById('contract_number').value = data.contractdata.contract_number;
            document.getElementById('rundate').value = data.contractdata.contract_rundate;
        }

    });

}

// ************************************************************************************************************************

function getcontracteditdata(id) {

    var value = id;

    $.ajax({
        url: "/contractDashboard/contractGetEditData",
        data: {
            'message': JSON.stringify(value),
        },
        success: function (data) {
            document.getElementById('contract_title').value = data.contractdata.contract_title;
            document.getElementById('contractor').value = data.contractdata.contract_contractor;
            document.getElementById('contract_type').value = data.contractdata.contract_type;
            document.getElementById('startdate').value = data.contractdata.contract_startdate;
            document.getElementById('project_name').value = data.contractdata.contract_projectname;
            document.getElementById('contract_code1').value = data.contractdata.contract_code;
            document.getElementById('contract_priode').value = data.contractdata.contract_period;
            document.getElementById('enddate').value = data.contractdata.contract_enddate;
            document.getElementById('warranty').value = data.contractdata.contract_warranty;
            document.getElementById('contract_number').value = data.contractdata.contract_number;
            document.getElementById('rundate').value = data.contractdata.contract_rundate;
        }

    });

}

//****************************************************************************************************************
function formatNumber(input) {

    let value = input.value.replace(/\D/g, '');
    value = value.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    input.value = value;
}

//*************************************************************************************************************
$(document).ready(function () {
    $.ajax({
        url: "/pmsDashboard/systemList",
        success: function (data) {
            systemSelect = document.getElementById('systemlist');
            systemSelect.options[systemSelect.options.length] = new Option('...', 0);
            for (var i = 0; i < data.system.length; i++) {
                systemSelect = document.getElementById('systemlist');
                systemSelect.options[systemSelect.options.length] = new Option(data.system[i], data.system_code[i]);

            }
        }
    });
});
//*************************************************************************************************************
function conPriceSel(){
    var value = document.getElementById('con_price_sel').value;

    if (value == 1){
        document.getElementById('contract_price2').style.display='';
        document.getElementById('contract_price3').style.display='none';
        document.getElementById('contract_price4').style.display='none';
        document.getElementById('Pre_pay_display').style.display='';

    }else if(value == 2){
        document.getElementById('contract_price2').style.display='none';
        document.getElementById('contract_price3').style.display='';
        document.getElementById('contract_price4').style.display='none';
        document.getElementById('Pre_pay_display').style.display='';

    }else if (value == 3){
        document.getElementById('contract_price2').style.display='none';
        document.getElementById('contract_price3').style.display='none';
        document.getElementById('contract_price4').style.display='';
        document.getElementById('Pre_pay_display').style.display='';

    }

}
//*************************************************************************************************************
$(document).ready(function () {

        const rows = document.querySelectorAll('tbody tr');
        rows.forEach(row => {
            row.addEventListener('click', function () {
                rows.forEach(r => r.classList.remove('selected'));
                this.classList.add('selected');
            });
        });

});
