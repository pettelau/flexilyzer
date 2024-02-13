"use client";
import { boolComponent } from "@/types/componentDefinitions";

import { Card, CardBody, CardHeader } from "@nextui-org/react";
import { Chip } from "@nextui-org/react";

export default function BoolComponent({ keyName, value }: boolComponent) {
  return (
    <Card className='w-[200px] px-4'>
      <CardBody className='flex flex-row justify-between items-center '>
        <div>{keyName}</div>
        <div>
          <Chip variant='bordered' color={value ? "success" : "danger"}>
            {value ? "Yes" : "No"}
          </Chip>
        </div>
      </CardBody>
    </Card>
  );
}
