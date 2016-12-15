Router.route('/');

/**
 * router to list all questions
 */
Router.route('/questions');

/**
 * router to retrieve info about particular question
 */
Router.route('/questions/:_id');

/**
 * router to create a question
 */
Router.route('/admin/create');