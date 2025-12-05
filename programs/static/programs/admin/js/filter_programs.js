// Wait for Django admin to load jQuery
if (typeof django !== "undefined" && typeof django.jQuery !== "undefined") {
  (function ($) {
    console.log("Filter programs script loaded");

    $(document).ready(function () {
      console.log("Document ready");

      var $university = $("#id_university");
      var $program = $("#id_program");

      console.log("University field found:", $university.length);
      console.log("Program field found:", $program.length);

      if (!$university.length || !$program.length) {
        console.log("Fields not found, exiting");
        return;
      }

      // Store all programs initially
      var allPrograms = [];
      $program.find("option").each(function () {
        allPrograms.push({
          value: $(this).val(),
          text: $(this).text(),
        });
      });
      console.log("All programs stored:", allPrograms.length);

      function filterPrograms() {
        var universityId = $university.val();
        console.log("Filtering for university ID:", universityId);

        var currentProgramId = $program.val();

        // Clear current options
        $program.empty();

        // Add empty option
        $program.append(
          $("<option>", {
            value: "",
            text: "---------",
          })
        );

        if (!universityId) {
          console.log("No university selected, showing all programs");
          // If no university selected, show all programs
          $.each(allPrograms, function (i, program) {
            if (program.value) {
              $program.append(
                $("<option>", {
                  value: program.value,
                  text: program.text,
                })
              );
            }
          });
        } else {
          console.log("Fetching programs from server...");
          // Fetch programs for selected university
          $.ajax({
            url: "/admin/programs/academicintake/filter-programs/",
            data: {
              university_id: universityId,
            },
            success: function (data) {
              console.log("Received programs:", data.length);
              $.each(data, function (i, program) {
                $program.append(
                  $("<option>", {
                    value: program.id,
                    text: program.name,
                    selected: program.id == currentProgramId,
                  })
                );
              });
            },
            error: function (xhr, status, error) {
              console.error("Error fetching programs:", error);
              console.error("Status:", status);
              console.error("Response:", xhr.responseText);
            },
          });
        }
      }

      // Filter when university changes
      $university.on("change", function () {
        console.log("University changed");
        filterPrograms();
      });

      // Initial filter if university is already selected
      if ($university.val()) {
        console.log("Initial university value:", $university.val());
        filterPrograms();
      }
    });
  })(django.jQuery);
} else {
  console.error(
    "Django jQuery not found. Make sure this script loads after Django admin scripts."
  );
}
