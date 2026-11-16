import assert from "node:assert/strict";
import test from "node:test";
import { emailForUsername, normalizeUsername } from "@/lib/usernames";

test("usuario ignora maiuscula e acento", () => {
  assert.equal(normalizeUsername("  Bárbara "), "barbara");
  assert.equal(normalizeUsername("BARBARA"), "barbara");
  assert.equal(emailForUsername("Léo"), "leo@casa-control.local");
  assert.equal(emailForUsername("barbara"), "barbara@casa-control.local");
  assert.equal(emailForUsername("Jonas"), "jonas@casa-control.local");
});

test("usuario desconhecido nao vira e-mail", () => {
  assert.equal(emailForUsername("visitante"), null);
  assert.equal(emailForUsername(""), null);
});
