import api from "@/utils/apiUtils";
import AssignmentAnalyzer from "@/components/assignmentComponents/AssignmentAnalyzer";
import AssignmentMetadata from "@/components/assignmentComponents/AssignmentMetadata";
import ConnectAssignmentAnalyzer from "@/components/assignmentComponents/ConnectAssignmentAnalyzer";

interface Props {
  params: { course_id: number; assignment_id: number };
}

export default async function AssignmentDetails({ params }: Props) {
  const analyzers = await api.getAssignmentAnalyzers(params.assignment_id, {
    cache: "no-cache",
  });

  const assignment_metadata = await api.getAssignmentMetadata(
    params.assignment_id,
  );

  if (!assignment_metadata.ok) {
    return "something wrong";
  }

  return (
    <>
      <div className="grow">
        <AssignmentMetadata metadata={assignment_metadata.data} />
      </div>
      <div className="my-8 flex flex-col items-center justify-center text-center">
        <h3 className="h3">Connected analyzers:</h3>
        <ConnectAssignmentAnalyzer
          assignment_id={params.assignment_id}
          connected_analyzers={analyzers.data}
        />
      </div>
      <div className="flex max-w-[1500px] space-x-4 overflow-x-auto p-2">
        {analyzers.data.map((analyzer) => {
          return (
            <>
              <AssignmentAnalyzer
                analyzer_id={analyzer.id}
                analyzer_name={analyzer.name}
                assignment_id={Number(params.assignment_id)}
              />
            </>
          );
        })}
      </div>
    </>
  );
}
