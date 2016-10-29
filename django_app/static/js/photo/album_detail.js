function photoLike(photoPk, likeType) {
    var url = '/photo/ajax/photo/' + photoPk + '/' + likeType + '/' ;
    $.ajax({
        method: 'POST',
        url: url,
    })
        .done(function(response) {
            console.log(response);
            var likeCount = response.like_count;
            var userLike = response.user_like;
            var spanLikeCount = $('#photo-' + photoPk + '-like-count');
            spanLikeCount.text(likeCount);

            var btnLike = $('#btn-photo-' + photoPk + '-like');

            if(userLike) {
                btnLike.addClass('label-info');
                btnLike.removeClass('label-default');
            } else {
                btnLike.removeClass('label-info');
                btnLike.addClass('label-default');
            }


            var dislikeCount = response.dislike_count;
            var userDislike = response.user_dislike;
            var spanDislikeCount = $('#photo-' + photoPk + '-dislike-count');
            spanDislikeCount.text(dislikeCount);

            var btnDislike = $('#btn-photo-' + photoPk + '-dislike');

            if(userDislike) {
                btnDislike.addClass('label-danger');
                btnDislike.removeClass('label-default');
            } else {
                btnDislike.removeClass('label-danger');
                btnDislike.addClass('label-default');
            }

        })
        .fail(function (response) {
            console.log(response);
        });
}