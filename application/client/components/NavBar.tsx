"use client";
import React, { useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import {
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  Link,
  Button,
  NavbarMenuToggle,
  NavbarMenu,
  NavbarMenuItem,
} from "@nextui-org/react";
import Image from "next/image";

export default function NavBar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const pathName = usePathname();

  const router = useRouter();

  const menuItems = [
    { display: "Courses", href: "/courses" },
    { display: "Analyzers", href: "/analyzers" },
    { display: "Guides", href: "/guides" },
    { display: "About", href: "/about" },
  ];

  return (
    <Navbar onMenuOpenChange={setIsMenuOpen}>
      <NavbarContent>
        <NavbarMenuToggle
          aria-label={isMenuOpen ? "Close menu" : "Open menu"}
          className="sm:hidden"
        />
        <NavbarBrand
          className="w-[50px] cursor-pointer"
          onClick={() => {
            router.push("/");
          }}
        >
          <Image
            width="0"
            height="0"
            sizes="100vw"
            className="hidden md:h-auto md:w-[170px] md:flex"
            alt="Flexilyzer logo"
            src="/flexilyzer.png"
          ></Image>
          <Image
            width="0"
            height="0"
            sizes="100vw"
            className="h-auto w-[40px] md:hidden"
            alt="Flexilyzer logo"
            src="/flexilyzer_small.png"
          ></Image>
        </NavbarBrand>
      </NavbarContent>

      <NavbarContent className="hidden gap-4 sm:flex" justify="center">
        {menuItems.map((item) => (
          <NavbarItem
            key={item.display}
            isActive={pathName.startsWith(item.href)}
          >
            <Link color="foreground" href={item.href}>
              {item.display}
            </Link>
          </NavbarItem>
        ))}
      </NavbarContent>
      <NavbarItem>
        <Button as={Link} color="primary" href="/profile" variant="flat">
          Profile
        </Button>
      </NavbarItem>
      <NavbarMenu className="mt-5">
        {menuItems.map((item, index) => (
          <NavbarMenuItem key={`${item}-${index}`}>
            <Link
              color={"foreground"}
              className="w-full"
              href={item.href}
              size="lg"
            >
              {item.display}
            </Link>
          </NavbarMenuItem>
        ))}
      </NavbarMenu>
    </Navbar>
  );
}
