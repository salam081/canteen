(function ($) {
    "use strict";
    // Global Roster object to accumulate dates
    let Roster = { dates: [] };
    // Setup the calendar with the current date
    $(document).ready(function () {
      var date = new Date();
      var today = date.getDate();
      const selectedDatesInput = document.getElementById('selectedDate');

      // Set click handlers for DOM elements
      $(".right-button").click({ date: date }, next_year);
      $(".left-button").click({ date: date }, prev_year);
      $(".month").click({ date: date }, month_click);
      $("#add-button").click({ date: date }, new_event);
      // Set current month as active
      $(".months-row").children().eq(date.getMonth()).addClass("active-month");
      //set the dates array to empty
      $("#clear-button").click(function () {
      Roster.dates = [];
      $(".active-date").removeClass("active-date");
      console.log(Roster);
      })
      $("#confirm-button").click(function(){
        if (Roster.dates.length === 0) {
          alert('You cannot submit without selecting a date');
        }
      })
      init_calendar(date);
      var events = check_events(today, date.getMonth() + 1, date.getFullYear());
      show_events(events, months[date.getMonth()], today);
    });
  
    // Initialize the calendar by appending the HTML dates
    function init_calendar(date) {
      $(".tbody").empty();
      $(".events-container").empty();
      var calendar_days = $(".tbody");
      var month = date.getMonth();
      var year = date.getFullYear();
      var day_count = days_in_month(month, year);
      var row = $("<tr class='table-row'></tr>");
      var today = new Date(); // Current date
  
      // Set date to 1 to find the first day of the month
      date.setDate(1);
      var first_day = date.getDay();
  
      for (var i = 0; i < 35 + first_day; i++) {
          var day = i - first_day + 1;
  
          if (i % 7 === 0) {
              calendar_days.append(row);
              row = $("<tr class='table-row'></tr>");
          }
  
          if (i < first_day || day > day_count) {
              var curr_date = $("<td class='table-date nil'>" + "</td>");
              row.append(curr_date);
          } else {
              var curr_date = $("<td class='table-date'>" + day + "</td>");
              var dateToCheck = new Date(year, month, day);
              
              // Calculate events for the current day
              var events = check_events(day, month + 1, year);
  
              // Disable past dates
              if (dateToCheck < today && !(day === today.getDate() && month === today.getMonth() && year === today.getFullYear())) {
                  curr_date.addClass("disabled-date");
              } else {
                  // Check if this date is in the Roster.dates array
                  const formattedDate = `${day}/${months[month]}/${year}`;
                  if (Roster.dates.includes(formattedDate)) {
                      curr_date.addClass("active-date");
                  }
  
                  if (day === today && month === today.getMonth() && year === today.getFullYear()) {
                      curr_date.addClass("activee-date");
                      show_events(events, months[month], day);
                  }
  
                  if (events.length !== 0) {
                      curr_date.addClass("event-date");
                  }
  
                  curr_date.click(
                      { events: events, month: months[month], day: day, year: year },
                      date_click
                  );
              }
  
              row.append(curr_date);
          }
      }
  
      calendar_days.append(row);
      $(".year").text(year);
  }
  
    // Get the number of days in a given month/year
    function days_in_month(month, year) {
      var monthStart = new Date(year, month, 1);
      var monthEnd = new Date(year, month + 1, 1);
      return (monthEnd - monthStart) / (1000 * 60 * 60 * 24);
    }
  
    function padZero(num) {
      return num.toString().padStart(2, '0');
  }
  // Event handler for when a date is clicked
  function date_click(event) {
      $(".events-container").show(250);
      $("#dialog").hide(250);
      $(this).toggleClass("active-date");
  
      const day = event.data.day;
      const month = event.data.month;
      const year = event.data.year || new Date().getFullYear()
    
      const selectedDate = `${year}-${padZero(month)}-${padZero(day)}`;
    
      const dateIndex = Roster.dates.indexOf(selectedDate);
  
      if ($(this).hasClass("active-date")) {
          if (dateIndex === -1) {
              Roster.dates.push(selectedDate);
          }
      } else {
          if (dateIndex !== -1) {
              Roster.dates.splice(dateIndex, 1);
          }
      }
      console.log(Roster);
      show_events(event.data.events, month, day, year);
      updateSelectedDates(event);
  }

  function updateSelectedDates(event) {
    const selectedDatesInput = document.getElementById('selectedDate');
    const day = event.data.day;
      const month = event.data.month;
      const year = event.data.year || new Date().getFullYear()
    const selectedDate = Roster.dates.map(date => {
      if(typeof date === 'string'){
        const [year, month, day] = date.split('-');
        return `${year}-${padZero(parseInt(month))}-${padZero(parseInt(day))}`;
      }
      return date
    });
    selectedDatesInput.value = JSON.stringify(selectedDate);
    console.log("Selected dates value:", selectedDatesInput.value);
}

    // Event handler for when a month is clicked
    function month_click(event) {
      $(".events-container").show(250);
      $("#dialog").hide(250);
      var date = event.data.date;
      $(".active-month").removeClass("active-month");
      $(this).addClass("active-month");
      var new_month = $(".month").index(this);
      date.setMonth(new_month);
      init_calendar(date);
    }
  
    // Event handler for when the year right-button is clicked
    function next_year(event) {
      $("#dialog").hide(250);
      var date = event.data.date;
      var new_year = date.getFullYear() + 1;
      $("year").html(new_year);
      date.setFullYear(new_year);
      init_calendar(date);
    }
  
    // Event handler for when the year left-button is clicked
    function prev_year(event) {
      $("#dialog").hide(250);
      var date = event.data.date;
      var new_year = date.getFullYear() - 1;
      $("year").html(new_year);
      date.setFullYear(new_year);
      init_calendar(date);
    }
  
    // Event handler for clicking the new event button
    function new_event(event) {
      // if a date isn't selected then do nothing
      if ($(".active-date").length === 0) return;
      // remove red error input on click
      $("input").click(function () {
        $(this).removeClass("error-input");
      });
      // empty inputs and hide events
      $("#dialog input[type=text]").val("");
      $("#dialog input[type=number]").val("");
      $(".events-container").hide(250);
      $("#dialog").show(250);

    }
  
    // Adds a json event to event_data
    function new_event_json(name, count, date, day) {
      var event = {
        occasion: name,
        invited_count: count,
        year: date.getFullYear(),
        month: date.getMonth() + 1,
        day: day,
      };
      event_data["events"].push(event);
    }
  
    // Display all events of the selected date in card views
    function show_events(events, month, day, year) {
      // Clear the dates container
      $(".events-container").empty();
      $(".events-container").show(250);
      // If there are no events for this date, notify the user
      if (events.length === 0) {
        var event_card = $("<div class='event-card'></div>");
        var event_name = $(
          "<div class='event-name'>There are no events planned for " +
            month +
            " " +
            day +
            ".</div>"
        );
        $(event_card).css({ "border-left": "10px solid #FF1744" });
        $(event_card).append(event_name);
        $(".events-container").append(event_card);
      } else {
        // Go through and add each event as a card to the events container
        for (var i = 0; i < events.length; i++) {
          var event_card = $("<div class='event-card'></div>");
          var event_name = $(
            "<div class='event-name'>" + events[i]["occasion"] + ":</div>"
          );
          var event_count = $(
            "<div class='event-count'>" +
              events[i]["invited_count"] +
              " Invited</div>"
          );
          if (events[i]["cancelled"] === true) {
            $(event_card).css({
              "border-left": "10px solid #FF1744",
            });
            event_count = $("<div class='event-cancelled'>Cancelled</div>");
          }
          $(event_card).append(event_name).append(event_count);
          $(".events-container").append(event_card);
        }
      }
    }
  
    // Checks if a specific date has any events
    function check_events(day, month, year) {
      var events = [];
      for (var i = 0; i < event_data["events"].length; i++) {
        var event = event_data["events"][i];
        if (
          event["day"] === day &&
          event["month"] === month &&
          event["year"] === year
        ) {
          events.push(event);
        }
      }
      return events;
    }
  
    // Given data for events in JSON format
    var event_data = {
      events: [
        ]
    };
 
    const months = [
      "01",
      "02",
      "03",
      "04",
      "05",
      "06",
      "07",
      "08",
      "09",
      "10",
      "11",
      "12",
    ];
  })(jQuery);
  