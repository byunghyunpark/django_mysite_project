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

        })
        .fail(function (response) {
            console.log(response);
        });
}