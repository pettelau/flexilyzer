"use client";
import { textComponent } from "@/types/componentDefinitions";

import { Card, CardBody, CardHeader } from "@nextui-org/react";

export default function TextComponent({ keyName, value }: textComponent) {
  return (
    <Card className="max-w-[600px] min-w-[200px] px-4">
      <CardHeader className="flex flex-row justify-center font-semibold">
        {keyName}
      </CardHeader>
      <CardBody className="text-small text-center pt-0">{value}</CardBody>
    </Card>
  );
}
