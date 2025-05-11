function attachfile() {

    var value = document.getElementById('status').value;


    if (value == 'RJCT') {
        document.getElementById('attach').style.display = '';
    } else {
        document.getElementById('attach').style.display = 'none';
    }


}

//*********************************************************************************************************************
//  clicking serial input make disable number of material and vice versa
$(document).ready(function () {

    $("#serial")
        .on('input', function () {
            var activeFee = (this.value !== '') ? true : false;
            $('#typeNumber').prop('disabled', activeFee);
        })
        .trigger('input');
});

$(document).ready(function () {
    $("#typeNumber")
        .on('input', function () {
            var activeFee = (this.value > 0) ? true : false;
            $('#serial').prop('disabled', activeFee);
        })
        .trigger('input');
});

// ********************************************************************************************************************
function proccess() {
    var value = document.getElementById('function').value;

    if (value == 1) {
        document.getElementById('ordercompany').style.display = 'none';
        document.getElementById('montagecompany').style.display = '';
        // document.getElementById('montageloco').style.display='';
        // document.getElementById('montagestatus').style.display='';
        document.getElementById('status').disabled = false;
        document.getElementById("loco").disabled = false;


    } else if (value == 2) {
        document.getElementById('ordercompany').style.display = '';
        document.getElementById('montagecompany').style.display = 'none';
        // document.getElementById('montageloco').style.display='none';
        document.getElementById("loco").disabled = true;
        // document.getElementById('montagestatus').style.display='none';
        document.getElementById('status').disabled = true;

    }

}

// ********************************************************************************************************************
$(document).ready(function () {
    $.ajax({
        url: "/pmsDashboard/companyLocoList",
        success: function (data) {
            systemSelect = document.getElementById('company');
            systemSelect.options[systemSelect.options.length] = new Option('...', 0);
            var index = data.selected_company;
            for (var i = 0; i < data.company.length; i++) {
                systemSelect = document.getElementById('company');
                systemSelect.options[systemSelect.options.length] = new Option(data.company[i], data.company_code[i]);
                if (index == data.company[i]) {
                    document.getElementById("company").selectedIndex = (i + 1);
                }
            }

            locodata();
        }
    });
});

// ********************************************************************************************************************
function locodata() {
    document.getElementById('loco').innerHTML = ''
    var value = document.getElementById('company').value;


    $.ajax({

        url: "/pmsDashboard/locoDataList",
        data: {
            'message': JSON.stringify(value),
        },
        success: function (data) {

            systemSelect = document.getElementById('loco');
            systemSelect.options[systemSelect.options.length] = new Option('...', 0);
            var index = data.selecteddloco;
            for (var i = 0; i < data.loco.length; i++) {
                systemSelect = document.getElementById('loco');
                systemSelect.options[systemSelect.options.length] = new Option(data.loco[i], data.loco[i]);
                if (index == data.loco[i]) {
                    document.getElementById("loco").selectedIndex = (i + 1);
                }
            }

        }
    });
// document.getElementById('company_code_setting').innerHTML=value;
}

//*******************************************************************************************************************
$(document).ready(function () {
    $.ajax({
        url: "/pmsDashboard/systemList",
        success: function (data) {

            for (var i = 0; i < data.system.length; i++) {
                systemSelect = document.getElementById('system');
                systemSelect.options[systemSelect.options.length] = new Option(data.system[i], data.system_code[i]);

            }
            var index = data.selected;
            document.getElementById('system');
            for (var i = 0; i < data.depot.length; i++) {
                systemSelect = document.getElementById('place');
                systemSelect.options[systemSelect.options.length] = new Option(data.depot[i], data.depot[i]);
                if (index == data.system_code[i]) {
                    document.getElementById("system").selectedIndex = (i + 1);
                }

            }
            systemdata();
        }
    });
});

// **********************************************************************************************************************

function systemdata() {
    document.getElementById('part').innerHTML = ''
    var value = document.getElementById('system').value;

    $.ajax({

        url: "/pmsDashboard/partList",
        data: {
            'message': JSON.stringify(value),
        },
        success: function (data) {
            systemSelect = document.getElementById('part');
            systemSelect.options[systemSelect.options.length] = new Option('...', 0);
            var selected = data.selectedpart;
            for (var i = 0; i < data.part.length; i++) {
                systemSelect = document.getElementById('part');
                systemSelect.options[systemSelect.options.length] = new Option(data.part[i], data.part_code[i]);
                if (selected == data.part_code[i]) {
                    document.getElementById("part").selectedIndex = (i + 1);
                }
            }

        }
    });

}

// ********************************************************************************************************************
function serialList() {
    var options = '';
    document.getElementById('serial').innerHTML = ''
    var value = document.getElementById('part').value;
    var system = document.getElementById('system').value;

    $.ajax({

        url: "/pmsDashboard/serialList",
        data: {
            'message': JSON.stringify(value),
            'system': JSON.stringify(system),
        },
        success: function (data) {

            for (var i = 0; i < data.serial.length; i++) {
                options += '<option>' + data.serial[i] + '</option>';
            }

            document.getElementById('list-timezone').innerHTML = options;

        }
    });


}

// ****************************************************************************************************************
document.addEventListener('DOMContentLoaded', e => {
    $('#serial').autocomplete()
}, false);

// ****************************************************************************************************************
function getcmt_check(id) {
    var value = id
    $.ajax({
        type: "GET",
        url: "/pmsDashboard/pmsCheck_desc",
        data: {
            'message': JSON.stringify(value),
        },
        success: function (data) {

            $("#desc").html(data.montagedesc);
            $("#register").html(data.checkdesc);

        }
    });
}

//*****************************************************************************************************************
// function checkfailedit(id) {
//     var value = id
//     $.ajax({
//         type: "GET",
//         url: "/pmsDashboard/pmsCheck_failEdit",
//         data: {
//             'message': JSON.stringify(value),
//         },
//         success: function (data) {
//
//             // $("#from_date").html(data.info.demontage_date);
//             document.getElementById('from_date').value = data.info.demontage_date
//             // $("#register").html(data.checkdesc);
//
//         }
//     });
// }

//*******************************************************************************************************************
function contractorList(id) {

    $.ajax({

        url: "/pmsDashboard/contractorDataList",
        data: {
            'message': JSON.stringify(id),
        },
        success: function (data) {
            var name = 'con' + id
            optionSelect = document.getElementById(name).options.length;

            if (optionSelect == 0) {

                for (var i = 0; i < data.contractor.length; i++) {
                    systemSelect = document.getElementById(name);
                    systemSelect.options[systemSelect.options.length] = new Option(data.contractor[i], data.contractor_code[i]);
                }
            }
        }

    });
}

//*********************************************************************************************************************

function getcmt_maintenance(id) {
    var stat = 'repair'
    $.ajax({
        type: "GET",
        url: "/pmsDashboard/pmsMaintenance_desc",
        data: {
            'message': JSON.stringify(id),
            'stat': JSON.stringify(stat),

        },
        success: function (data) {
            $("#desc").html(data.montagedesc);
            $("#register").html(data.checkdesc);
        }
    });
}

//********************************************************************************************************************
function getcmt_warehouse(id) {
    var stat = $('.desc_but').attr('stat');

    $.ajax({
        type: "GET",
        url: "/pmsDashboard/pmsWarehouse_descEnter",
        data: {
            'message': JSON.stringify(id),
            'stat': JSON.stringify(stat),

        },
        success: function (data) {

            $("#desc").html(data.montagedesc);
            $("#register").html(data.checkdesc);
        }
    });

}

//*******************************************************************************************************************
function getcmt_underrepair(id) {
    var stat = 'repairwait'
    $.ajax({
        type: "GET",
        url: "/pmsDashboard/pmsWarehouse_descEnter",
        data: {
            'message': JSON.stringify(id),
            'stat': JSON.stringify(stat),

        },
        success: function (data) {

            $("#desc").html(data.montagedesc);
            $("#register").html(data.checkdesc);
        }
    });

}

//*******************************************************************************************************************
function getcmt_senttowarehouse(id) {
    var stat = 'repairwait'
    $.ajax({
        type: "GET",
        url: "/pmsDashboard/pmsWarehouse_descEnter",
        data: {
            'message': JSON.stringify(id),
            'stat': JSON.stringify(stat),

        },
        success: function (data) {

            $("#desc").html(data.montagedesc);
            $("#register").html(data.checkdesc);
        }
    });
}

//****************************************************************************************************************
function getcmt_qc(id) {
    var stat = 'qc'
    $.ajax({
        type: "GET",
        url: "/pmsDashboard/pmsQc_desc",
        data: {
            'message': JSON.stringify(id),
            'stat': JSON.stringify(stat),

        },
        success: function (data) {

            $("#desc").html(data.montagedesc);
            $("#register").html(data.checkdesc);
        }
    });
}

//*************************************************************************************************************
$(document).ready(function () {
    $.ajax({

        url: "/pmsDashboard/settingscompany_list",
        success: function (data) {


            systemSelect = document.getElementById('company_name');
            systemSelect.options[systemSelect.options.length] = new Option('...', 0);
            for (var i = 0; i < data.company.length; i++) {
                systemSelect = document.getElementById('company_name');
                systemSelect.options[systemSelect.options.length] = new Option(data.company[i], data.id[i]);
            }

        }
    });
});

//***********************************************************************************************************
function contractdetail() {

    document.getElementById("system_list").disabled = true;
    document.getElementById("table_visibility").style.display = 'none';

    var value = document.getElementById('company_name').value;

    $.ajax({

        url: "/pmsDashboard/settingscompany_code",
        data: {
            'message': JSON.stringify(value),
        },
        success: function (data) {

            document.getElementById("system_list").disabled = false;

            systemlistfunc();

        }
    });

}

//*********************************************************************************************************
function getcontractdatapms(id) {
    var value = id;
    $.ajax({
        url: "/pmsDashboard/settingscontract_data",
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

//*******************************************************************************************************************
function systemlistfunc() {
    $.ajax({
        url: "/pmsDashboard/systemList",
        success: function (data) {
            systemSelect = document.getElementById('system_list');
            systemSelect.options[systemSelect.options.length] = new Option('...', 0);
            for (var i = 0; i < data.system.length; i++) {
                systemSelect = document.getElementById('system_list');
                systemSelect.options[systemSelect.options.length] = new Option(data.system[i], data.system_code[i]);

            }
        }
    });
};

//********************************************************************************************************************

function getpartlist() {

    var value = document.getElementById('system_list').value;

    $.ajax({

        url: "/pmsDashboard/schedule_data",
        data: {
            'message': JSON.stringify(value),
        },
        success: function (data) {

            const rows = data.rows;
            document.getElementById("table_visibility").style.display = '';

            //clear table content
            const tbody = document.getElementById('schedule-table');
            tbody.innerHTML = '';


            const table = document.getElementById('schedule-table');


            rows.forEach(row => {
                const tr = document.createElement('tr');


                row.forEach(schedule => {


                    const tdCheckbox = document.createElement('td');
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.checked = schedule.is_selected;
                    checkbox.name = 'is_selected_' + schedule.part_code;
                    tdCheckbox.appendChild(checkbox);
                    tr.appendChild(tdCheckbox);


                    const tdPeriod = document.createElement('td');
                    tdPeriod.textContent = schedule.part;
                    tr.appendChild(tdPeriod);


                    const tdDash = document.createElement('td');
                    const input = document.createElement('input');
                    input.type = 'number';
                    input.name = 'text_field_' + schedule.part_code;
                    input.className = 'form-control';
                    input.setAttribute('style', 'width: 8rem;')
                    input.placeholder = 'گارانتی';
                    input.min = '30';
                    input.max = '2000';
                    input.step = '30';
                    tdDash.appendChild(input);
                    tr.appendChild(tdDash);


                });


                if (row.length < 3) {
                    for (let i = row.length; i < 3; i++) {
                        const tdCheckbox = document.createElement('td');
                        const checkbox = document.createElement('input');
                        checkbox.type = 'checkbox';
                        checkbox.disabled = true;
                        tdCheckbox.appendChild(checkbox);
                        tr.appendChild(tdCheckbox);

                        const tdDash = document.createElement('td');
                        tdDash.textContent = '-';
                        tr.appendChild(tdDash);

                        const tdPeriod = document.createElement('td');
                        tdPeriod.textContent = '-';
                        tr.appendChild(tdPeriod);
                    }
                }

                table.appendChild(tr);
            });
        }
    });

}

//*******************************************************************************************************************
$(document).ready(function () {

    const rows = document.querySelectorAll('tbody tr');
    rows.forEach(row => {
        row.addEventListener('click', function () {
            rows.forEach(r => r.classList.remove('selected'));
            this.classList.add('selected');
        });
    });

});

// ****************************************************************************************************************
function submitForm(formId, formAction) {

    const form = document.getElementById('form-' + formId);
    if (form) {

        form.action = formAction;
        form.method = 'post';
        form.submit();
    }
}

// ********************************************************************************************************************
$(document).ready(function () {
    $.ajax({
        url: "/pmsDashboard/companyLocoList",
        success: function (data) {
            systemSelect = document.getElementById('editcompany');
            systemSelect.options[systemSelect.options.length] = new Option('...', 0);
            var index = data.selected_company;
            for (var i = 0; i < data.company.length; i++) {
                systemSelect = document.getElementById('editcompany');
                systemSelect.options[systemSelect.options.length] = new Option(data.company[i], data.company_code[i]);
                if (index == data.company[i]) {
                    document.getElementById("editcompany").selectedIndex = (i + 1);
                }
            }

            locodata();
        }
    });
});

//********************************************************************************************************************
$(document).ready(function () {
    $.ajax({
        url: "/pmsDashboard/companyLocoList",
        success: function (data) {
            systemSelect0 = document.getElementById('delcompany');
            systemSelect4 = document.getElementById('editcompany1');
            systemSelect1 = document.getElementById('delcompanylist');
            systemSelect2 = document.getElementById('addcompanylist');
            systemSelect3 = document.getElementById('editcompanylist');
            systemSelect0.options[systemSelect0.options.length] = new Option('...', 0);
            systemSelect4.options[systemSelect4.options.length] = new Option('...', 0);
            systemSelect1.options[systemSelect1.options.length] = new Option('...', 0);
            systemSelect2.options[systemSelect2.options.length] = new Option('...', 0);
            systemSelect3.options[systemSelect3.options.length] = new Option('...', 0);

            for (var i = 0; i < data.company.length; i++) {
                systemSelect0 = document.getElementById('delcompany');
                systemSelect4 = document.getElementById('editcompany1');
                systemSelect1 = document.getElementById('delcompanylist');
                systemSelect2 = document.getElementById('addcompanylist');
                systemSelect3 = document.getElementById('editcompanylist');
                systemSelect0.options[systemSelect0.options.length] = new Option(data.company[i], data.company_code[i]);
                systemSelect4.options[systemSelect4.options.length] = new Option(data.company[i], data.company_code[i]);
                systemSelect1.options[systemSelect1.options.length] = new Option(data.company[i], data.company_code[i]);
                systemSelect2.options[systemSelect2.options.length] = new Option(data.company[i], data.company_code[i]);
                systemSelect3.options[systemSelect3.options.length] = new Option(data.company[i], data.company_code[i]);

            }
        }
    });
});

// ********************************************************************************************************************
function locodatainfo1(value) {

    $.ajax({

        url: "/pmsDashboard/locoDataList",
        data: {
            'message': JSON.stringify(value),
        },
        success: function (data) {

            systemSelect0 = document.getElementById('dellocolist');
            systemSelect0.options[systemSelect0.options.length] = new Option('...', 0);


            for (var i = 0; i < data.loco.length; i++) {
                systemSelect0 = document.getElementById('dellocolist');
                systemSelect0.options[systemSelect0.options.length] = new Option(data.loco[i], data.loco[i]);
            }

        }
    });

}
// ********************************************************************************************************************
function locodatainfo2(value) {

    $.ajax({

        url: "/pmsDashboard/locoDataList",
        data: {
            'message': JSON.stringify(value),
        },
        success: function (data) {

            systemSelect0 = document.getElementById('editlocolist');
            systemSelect0.options[systemSelect0.options.length] = new Option('...', 0);


            for (var i = 0; i < data.loco.length; i++) {
                systemSelect0 = document.getElementById('editlocolist');
                systemSelect0.options[systemSelect0.options.length] = new Option(data.loco[i], data.loco[i]);
            }

        }
    });

}
//*******************************************************************************************************************
$(document).ready(function () {
    $.ajax({
        url: "/pmsDashboard/systemList",
        success: function (data) {

            systemSelect0 = document.getElementById('deldepot');
            systemSelect1 = document.getElementById('editdepot');
            systemSelect0.options[systemSelect0.options.length] = new Option('...', 0);
            systemSelect1.options[systemSelect1.options.length] = new Option('...', 0);

            for (var i = 0; i < data.depot.length; i++) {
                systemSelect0 = document.getElementById('deldepot');
                systemSelect1 = document.getElementById('editdepot');
                systemSelect0.options[systemSelect0.options.length] = new Option(data.depot[i], data.depot[i]);
                systemSelect1.options[systemSelect1.options.length] = new Option(data.depot[i], data.depot[i]);

            }

        }
    });
});
//******************************************************************************************************************
$(document).ready(function () {
    $.ajax({
        url: "/pmsDashboard/locodetailslist",
        success: function (data) {

            systemSelect0 = document.getElementById('dieselsel');
            systemSelect0.options[systemSelect0.options.length] = new Option('شماره لکوموتیو', 0);

            for (var i = 0; i < data.loco.length; i++) {
                systemSelect0 = document.getElementById('dieselsel');
                systemSelect0.options[systemSelect0.options.length] = new Option(data.loco[i], data.loco[i]);
            }
        }
    });
});

// *************************************************** show details modal code ********************************************

 $(document).ready(function () {
            $('.image-link').click(function (event) {
                event.preventDefault();
                var imageId = $(this).data('image-id');
                var action = $(this).data('action');
                fetchImage(imageId, action);
            });
        });


        function fetchImage(imageId, action) {
            $.ajax({
                url: "/pmsDashboard/getimage",
                data: {
                    'id': JSON.stringify(imageId),
                    'stat': JSON.stringify(action),
                },
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // برای شناسایی درخواست AJAX در جنگو
                },
                success: function (data) {
                    if (data.image_data) {
                        openModal(data.image_data);
                    } else {
                        alert('تصویر یافت نشد!');
                    }
                },
                error: function (xhr, status, error) {
                    console.error('خطا:', error);
                    alert('خطایی رخ داد!');
                }
            });
        }


        function openModal(base64Data) {
            var modal = document.getElementById('imageModal');
            var modalImg = document.getElementById('modalImage');
            modal.style.display = 'flex';
            modalImg.src = 'data:image/jpeg;base64,' + base64Data;
        }


        function closeModal() {
            var modal = document.getElementById('imageModal');
            modal.style.display = 'none';
        }


        function saveImage() {
            var modalImg = document.getElementById('modalImage');
            var link = document.createElement('a');
            link.href = modalImg.src;
            link.download = 'image.jpg';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }


        function printImage() {
            var modalImg = document.getElementById('modalImage');
            var printWindow = window.open('');
            printWindow.document.write('<html><body><img src="' + modalImg.src + '" style="width:100%;"></body></html>');
            printWindow.document.close();
            printWindow.print();
        }


        window.onclick = function (event) {
            var modal = document.getElementById('imageModal');
            if (event.target === modal) {
                closeModal();
            }
        };

 // ************************************************************ qc image modal *********************************************

 // افزودن رویداد کلیک به لینک‌ها
        $(document).ready(function () {
            $('.qc-pic').click(function (event) {
                event.preventDefault();
                var imageId = $(this).data('image-id');
                var action = $(this).data('action');
                qcImage(imageId, action);
            });
        });

        // ارسال درخواست AJAX برای دریافت تصویر
        function qcImage(imageId, action) {
            $.ajax({
                url: "/pmsDashboard/openFile",
                data: {
                    'id': JSON.stringify(imageId),
                    'stat': JSON.stringify(action),
                },
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // برای شناسایی درخواست AJAX در جنگو
                },
                success: function (data) {
                    if (data.image_data) {
                        openModal(data.image_data);
                    } else {
                        alert('تصویر یافت نشد!');
                    }
                },
                error: function (xhr, status, error) {
                    console.error('خطا:', error);
                    alert('خطایی رخ داد!');
                }
            });
        }

        // باز کردن مودال و تنظیم تصویر
        function openModal(base64Data) {
            var modal = document.getElementById('imageModal');
            var modalImg = document.getElementById('modalImage');
            modal.style.display = 'flex';
            modalImg.src = 'data:image/jpeg;base64,' + base64Data;
        }

        // بستن مودال
        function closeModal() {
            var modal = document.getElementById('imageModal');
            modal.style.display = 'none';
        }

        // ذخیره (دانلود) تصویر
        function saveImage() {
            var modalImg = document.getElementById('modalImage');
            var link = document.createElement('a');
            link.href = modalImg.src;
            link.download = 'image.jpg';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        // چاپ تصویر
        function printImage() {
            var modalImg = document.getElementById('modalImage');
            var printWindow = window.open('');
            printWindow.document.write('<html><body><img src="' + modalImg.src + '" style="width:100%;"></body></html>');
            printWindow.document.close();
            printWindow.print();
        }

        // بستن مودال با کلیک روی پس‌زمینه
        window.onclick = function (event) {
            var modal = document.getElementById('imageModal');
            if (event.target === modal) {
                closeModal();
            }
        };