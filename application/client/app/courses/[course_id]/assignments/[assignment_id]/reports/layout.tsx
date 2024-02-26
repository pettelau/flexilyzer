import api from "@/utils/apiUtils";
import AssignmentSideBar from "@/components/assignmentComponents/SideBar";
import AnalyzerTabs from "@/components/reportPageComponents/AnalyzerTabs";

export default async function AssignmentLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: {
    course_id: number;
    assignment_id: number;
  };
}) {
  const assignment_analyzers = await api.getAssignmentAnalyzers(
    params.assignment_id,
    { cache: "no-cache" }
  );

  return (
    <>
      <div className='flex flex-row'>
        {/* Sidebar */}
        <AssignmentSideBar
          course_id={params.course_id}
          assignment_id={params.assignment_id}
        />
        <div className='grow'>
          <div className='flex flex-row justify-center'>
            <div className='mt-2'>
              <AnalyzerTabs
                assignment_analyzers={assignment_analyzers.data}
                course_id={params.course_id}
                assignment_id={params.assignment_id}
              />
            </div>
          </div>
          {children}
        </div>
      </div>
    </>
  );
}
