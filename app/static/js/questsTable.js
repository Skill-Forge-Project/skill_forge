// $(document).ready(function () {
//   $('#dtOrderExample').DataTable({
//     "order": [[ 3, "desc" ]]
//   });
//     $('.dataTables_length').addClass('bs-select');
// });

$(function () {
  $(document).ready(function () {
      $('#edit_quest_table').DataTable();
  });
});

// Table for user submited quests in the admin panel
$(function () {
  $(document).ready(function () {
      $('#submited_quests_table').DataTable();
  });
});

$(function () {
  $(document).ready(function () {
      $('#reported_quests_table').DataTable();
  });
});


// Table for quests
$(function () {
  $(document).ready(function () {
      $('#quests_table').DataTable();
  });
});


// Table for user submited quests in the user profile
$(function () {
  $(document).ready(function () {
    $('#user_submited_quests').DataTable();
  });
});

// Table for user solved quests
$(function () {
  $(document).ready(function () {
    $('#user_solved_quests').DataTable();
  });
});

// Table for editing users from admin panel
$(function () {
  $(document).ready(function () {
    $('#mange_users_table').DataTable();
  });
});

// Table for displaying the guilds list
$(function () {
  $(document).ready(function () {
    $('#guilds_list').DataTable();
  });
});