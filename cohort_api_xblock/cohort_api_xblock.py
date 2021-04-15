"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from django.utils import translation
from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.fragment import Fragment
from xblockutils.resources import ResourceLoader

from openedx.core.djangoapps.course_groups.cohorts import get_cohort
from opaque_keys.edx.keys import CourseKey

class CohortAPIXblock(XBlock):
    """
    Xblock used to get data about students cohorts.
    """

    cohort_name = String(
        default="Default cohort name",
        scope=Scope.user_state,
        help="Cohort name where the user belongs.",
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the CohortAPIXblock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/cohort_api_xblock.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/cohort_api_xblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/cohort_api_xblock.js"))
        frag.initialize_js('CohortAPIXblock')
        return frag

    def studio_view(self, context=None):
        """
        Returns author view fragment on Studio.
        Should display an example on how to use this xblock.
        """
        # pylint: disable=unused-argument, no-self-use
        html = self.resource_string("static/html/cohort_api_xblock_author.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/cohort_api_xblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/cohort_api_xblock.js"))
        frag.initialize_js('CohortAPIXblock')
        return frag

    @XBlock.json_handler
    def get_user_cohort(self, data, suffix=''):
        """
        Handler used to retrieve information about the students cohort, it uses the course that
        includes this component.
        """
        is_studio = hasattr(self.xmodule_runtime, "is_author_mode")  # pylint: disable=no-member

        if is_studio:
            return {}

        current_anonymous_student_id = self.runtime.anonymous_student_id
        user = self.runtime.get_real_user(current_anonymous_student_id)
        course_id_str = str(self.runtime.course_id)

        course_key = CourseKey.from_string(course_id_str)
        cohort = get_cohort(user, course_key, assign=False, use_cached=True)

        return {"cohort_name": cohort.name}

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("CohortAPIXblock",
             """<cohortapixblock/>
             """),
            ("Multiple CohortAPIXblock",
             """<vertical_demo>
                <cohortapixblock/>
                <cohortapixblock/>
                <cohortapixblock/>
                </vertical_demo>
             """),
        ]
