import { Badge as BadgePrimitive } from "@kobalte/core/badge";
import type { VariantProps } from "cva";
import type { ComponentProps, ValidComponent } from "solid-js";
import { splitProps } from "solid-js";

import { cva } from "@/lib/cva";

export const badgeVariants = cva({
  base: "inline-flex items-center justify-center rounded-md border px-2 py-0.5 text-[13px] font-medium w-fit whitespace-nowrap shrink-0 [&>svg]:size-3 gap-1 [&>svg]:pointer-events-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive transition-[color,box-shadow] overflow-hidden",
  variants: {
    variant: {
      default: "bg-primary text-primary-foreground [a]:hover:bg-primary/80",
      warning:
        "border-yellow-400 bg-yellow-100 text-yellow-700 dark:border-yellow-700 dark:bg-yellow-900 dark:text-yellow-300",
      success:
        "border-green-300 bg-green-100 text-green-800 dark:border-green-700 dark:bg-green-900 dark:text-green-300",
      destructive:
        "border-destructive/40 bg-destructive/10 text-destructive focus-visible:ring-destructive/20 dark:border-destructive/60 dark:bg-destructive/20 dark:focus-visible:ring-destructive/40 [a]:hover:bg-destructive/20",
    },
  },
  defaultVariants: {
    variant: "default",
  },
});

export type BadgeProps<T extends ValidComponent = "span"> = ComponentProps<
  typeof BadgePrimitive<T>
> &
  VariantProps<typeof badgeVariants>;

export function Badge<T extends ValidComponent = "span">(props: BadgeProps<T>) {
  const [, rest] = splitProps(props as BadgeProps, ["class", "variant"]);

  return (
    <BadgePrimitive
      data-slot="badge"
      class={badgeVariants({
        variant: props.variant,
        class: props.class,
      })}
      {...rest}
    />
  );
}
