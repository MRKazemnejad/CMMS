
// **************************************** diesel details filter ******************************************************
function populateFilters() {
            const table = document.getElementById("dataTable");
            const rows = table.getElementsByTagName("tr");
            const selects = document.querySelectorAll(".table-filter select");
            const uniqueValues = Array.from({ length: 7 }, () => new Set()); // 7 ستون با فیلتر

            console.log("Rows found:", rows.length); // دیباگ تعداد ردیف‌ها

            // جمع‌آوری داده‌های منحصربه‌فرد برای 7 ستون اول
            for (let i = 0; i < rows.length; i++) {
                const cells = rows[i].getElementsByTagName("td");
                if (cells.length === 8) { // فقط ردیف‌های با 8 سلول
                    for (let j = 0; j < 7; j++) { // فقط 7 ستون اول
                        const textValue = cells[j].textContent.trim();
                        if (textValue && textValue !== "-" && textValue !== "داده‌ای برای نمایش وجود ندارد") {
                            uniqueValues[j].add(textValue);
                        }
                    }
                }
            }

            console.log("Unique values:", uniqueValues); // دیباگ مقادیر منحصربه‌فرد

            // پر کردن منوهای کشویی
            selects.forEach((select, index) => {
                select.innerHTML = '<option value="">همه</option>';
                uniqueValues[index].forEach(value => {
                    const option = document.createElement("option");
                    option.value = value;
                    option.textContent = value;
                    select.appendChild(option);
                });
            });
        }

        function filterTable(column, select) {
            const filter = select.value;
            const table = document.getElementById("dataTable");
            const rows = table.getElementsByTagName("tr");

            for (let i = 0; i < rows.length; i++) {
                const cell = rows[i].getElementsByTagName("td")[column];
                if (cell) {
                    const textValue = cell.textContent.trim();
                    rows[i].style.display = filter === "" || textValue === filter ? "" : "none";
                }
            }
        }

        // اجرای تابع پر کردن فیلترها بعد از رندر کامل DOM
        document.addEventListener("DOMContentLoaded", () => {
            populateFilters();
        });

// *********************************************************************************************************************