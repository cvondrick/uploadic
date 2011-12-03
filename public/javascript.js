$(document).ready(function()
{
    // check if the worker has accepted the job or not.
    // if they haven't, we must remind them to accept.
    // otherwise, we will show them statistics we have collected on them.
    if (!mturk_isassigned())
    {
        mturk_acceptfirst();

        $("#submitbutton").after("<strong>Accept task first!</strong>")
        $("#submitbutton").remove();
    }
    else
    {
        mturk_showstatistics();
    }

    // get the job id
    var parameters = mturk_parameters();
    if (!parameters["id"])
    {
        death("Missing Job Id")
        return;
    }

    // request to the server for the activities in this job
    server_request("getjob", [parameters["id"]], function(data) {
        eventlog("request", "Got the job");
        for (var i in data.activities)
        {
            // inject activities into the user interface
            $("#activities").append("<li>" + data.activities[i] + "</li>");
        }
    });

    // create a trigger for when the form is submitted
    $("#form").submit(function() {
        if ($("#video").val() == "")
        {
            window.alert("Please select a file first.");
            return;
        }

        eventlog("upload", "Starting upload");

        // update status for the user to know it's uploading
        $("#form").hide();
        $("#working").show();
        $("#errored").hide();
    })

    // change the upload target
    $("#form").attr("action", "server/upload/" + parameters["id"]);
});

function uploaded()
{
    // this is called after the upload is done. it notifies the worker that
    // the upload was complete, then redirects after 1 second to the
    // MTurk callback.

    return;

    eventlog("upload", "Upload success");

    $("#working").hide();
    $("#success").show();

    window.setTimeout(function() {
        mturk_submit(function(redirect) {
            redirect();
        });
    }, 100);
}

function errored(message)
{
    // this is called after the upload is done, but it failed. it allows the
    // worker to attempt to upload again.

    eventlog("upload", "Upload failed!");

    $("#working").hide();
    $("#errored").html(message).show();
    $("#form").show();
}
